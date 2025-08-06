from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import newspaper
from bs4 import BeautifulSoup
import requests
import re
import uuid
from config import GEMINI_API_KEY, MAX_SUMMARY_PER_SESSION, MAX_QA_PER_SESSION, ALLOWED_ORIGINS
from database import UsageTracker

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Configure CORS
CORS(app, origins=ALLOWED_ORIGINS, supports_credentials=True)

# Initialize Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize usage tracker
usage_tracker = UsageTracker()

def extract_article_content(url):
    """Extract article content from URL using newspaper3k and BeautifulSoup as fallback"""
    try:
        # Try newspaper3k first
        article = newspaper.Article(url)
        article.download()
        article.parse()
        
        if article.text and len(article.text.strip()) > 100:
            return {
                'title': article.title,
                'content': article.text,
                'success': True
            }
    except Exception as e:
        print(f"Newspaper3k failed: {e}")
    
    try:
        # Fallback to BeautifulSoup
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "Article"
        
        # Extract main content
        # Try common article content selectors
        content_selectors = [
            'article',
            '[class*="content"]',
            '[class*="article"]',
            '[class*="post"]',
            'main',
            '.entry-content',
            '.post-content',
            '.article-content'
        ]
        
        content = ""
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                content = ' '.join([elem.get_text().strip() for elem in elements])
                if len(content) > 200:
                    break
        
        # If no content found, use body text
        if not content or len(content) < 200:
            content = soup.get_text()
        
        # Clean up content
        content = re.sub(r'\s+', ' ', content).strip()
        
        if len(content) > 100:
            return {
                'title': title_text,
                'content': content,
                'success': True
            }
        
    except Exception as e:
        print(f"BeautifulSoup failed: {e}")
    
    return {
        'title': "Error",
        'content': "Could not extract article content",
        'success': False
    }

def generate_summary(content, title):
    """Generate summary using Gemini AI"""
    try:
        # Limit content to stay within free tier limits (roughly 4000 tokens)
        max_content_length = 3000  # Reduced from 8000 to stay within free limits
        truncated_content = content[:max_content_length]
        
        prompt = f"""
        Please provide a brief summary of the following article:
        
        Title: {title}
        
        Content:
        {truncated_content}
        
        Please provide a concise summary (around 150-200 words) that captures the main points.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API error: {e}")
        return "Error generating summary. Please try again."

def answer_question(question, summary, content):
    """Answer follow-up question using Gemini AI"""
    try:
        # Limit content to stay within free tier limits
        max_content_length = 2000  # Reduced for Q&A to stay within limits
        truncated_content = content[:max_content_length]
        
        prompt = f"""
        Based on the following article summary and content, please answer this question:
        
        Article Summary:
        {summary}
        
        Original Article Content (for reference):
        {truncated_content}
        
        Question: {question}
        
        Please provide a brief, accurate answer based on the information in the article.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API error: {e}")
        return "Error generating answer. Please try again."

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'AI Article Summarizer API is running'})

@app.route('/summarize', methods=['POST'])
def summarize_article():
    """Summarize article from URL"""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url'].strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Check session limits
        session = usage_tracker.get_or_create_session(session_id)
        if session['summary_count'] >= MAX_SUMMARY_PER_SESSION:
            return jsonify({
                'error': f'Summary limit reached. Maximum {MAX_SUMMARY_PER_SESSION} summary per session.',
                'session_id': session_id
            }), 429
        
        # Check if article is already cached
        cached_article = usage_tracker.get_article(url)
        if cached_article:
            return jsonify({
                'summary': cached_article['summary'],
                'title': cached_article['title'],
                'session_id': session_id,
                'cached': True
            })
        
        # Extract article content
        article_data = extract_article_content(url)
        if not article_data['success']:
            return jsonify({'error': 'Could not extract article content'}), 400
        
        # Generate summary
        summary = generate_summary(article_data['content'], article_data['title'])
        
        # Save to database
        usage_tracker.save_article(url, article_data['title'], article_data['content'], summary, session_id)
        usage_tracker.increment_summary_count(session_id)
        
        return jsonify({
            'summary': summary,
            'title': article_data['title'],
            'session_id': session_id,
            'cached': False
        })
        
    except Exception as e:
        print(f"Error in summarize endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    """Answer follow-up question about the article"""
    try:
        data = request.get_json()
        
        if not data or 'question' not in data or 'url' not in data:
            return jsonify({'error': 'Question and URL are required'}), 400
        
        question = data['question'].strip()
        url = data['url'].strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not question:
            return jsonify({'error': 'Question cannot be empty'}), 400
        
        # Check session limits
        session = usage_tracker.get_or_create_session(session_id)
        if session['qa_count'] >= MAX_QA_PER_SESSION:
            return jsonify({
                'error': f'Q&A limit reached. Maximum {MAX_QA_PER_SESSION} questions per session.',
                'session_id': session_id
            }), 429
        
        # Get cached article
        cached_article = usage_tracker.get_article(url)
        if not cached_article:
            return jsonify({'error': 'No article found. Please summarize an article first.'}), 400
        
        # Generate answer
        answer = answer_question(question, cached_article['summary'], cached_article['content'])
        
        # Increment usage count
        usage_tracker.increment_qa_count(session_id)
        
        return jsonify({
            'answer': answer,
            'session_id': session_id
        })
        
    except Exception as e:
        print(f"Error in ask endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/session-status', methods=['GET'])
def get_session_status():
    """Get current session usage status"""
    try:
        session_id = request.args.get('session_id')
        if not session_id:
            return jsonify({'error': 'Session ID is required'}), 400
        
        session = usage_tracker.get_or_create_session(session_id)
        
        return jsonify({
            'session_id': session['session_id'],
            'summary_count': session['summary_count'],
            'qa_count': session['qa_count'],
            'max_summary': MAX_SUMMARY_PER_SESSION,
            'max_qa': MAX_QA_PER_SESSION
        })
        
    except Exception as e:
        print(f"Error in session-status endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Clean up old sessions on startup
    usage_tracker.cleanup_old_sessions()
    
    print("🚀 AI Article Summarizer API starting...")
    print(f"📊 Max summary per session: {MAX_SUMMARY_PER_SESSION}")
    print(f"❓ Max Q&A per session: {MAX_QA_PER_SESSION}")
    print("🌐 Server running on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 