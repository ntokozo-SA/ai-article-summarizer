# AI-Powered Article Summarizer Chrome Extension

#### Video Demo:  https://www.youtube.com/watch?v=p9kwXsW-RJQ&ab

#### Description:
A sophisticated Chrome Extension that leverages Google Gemini AI to provide intelligent article summarization and interactive Q&A capabilities. Built with modern web technologies and designed for seamless user experience.

## 🚀 Live Demo & Features

- **Smart Article Summarization**: Extract and summarize content from any webpage using advanced AI
- **Interactive Q&A**: Ask contextual follow-up questions about summarized articles
- **Usage Management**: Session-based limits to control API costs and prevent abuse
- **Modern UI/UX**: Beautiful, responsive Chrome Extension interface
- **Real-time Processing**: Instant AI-powered insights with loading states
- **Cross-platform**: Works on any website with article content

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern UI framework with hooks
- **Webpack 5** - Module bundling and optimization
- **CSS3** - Modern styling with gradients and animations
- **Chrome Extension API** - Browser integration

### Backend
- **Flask 2.3** - Lightweight Python web framework
- **Google Gemini AI** - Advanced language model for content processing
- **SQLite3** - Lightweight database for session management
- **Newspaper3k** - Intelligent article extraction
- **BeautifulSoup4** - HTML parsing and content cleaning

### Key Libraries
- `google-generativeai` - Gemini AI integration
- `flask-cors` - Cross-origin resource sharing
- `requests` - HTTP client for web scraping
- `lxml` - XML/HTML processing

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Google Gemini API key
- Chrome browser

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-article-summarizer.git
cd ai-article-summarizer
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure API Key
Edit `backend/config.py` and add your Gemini API key:
```python
GEMINI_API_KEY = "your_actual_gemini_api_key_here"
```

### 4. Start Backend Server
```bash
python app.py
```
Server runs on `http://localhost:5000`

### 5. Frontend Setup
```bash
cd extension
npm install
npm run build
```

### 6. Install Chrome Extension
1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select `extension/dist` folder

## 🎯 Usage

1. **Navigate to any article or documentation page**
2. **Click the extension icon** in Chrome toolbar
3. **Paste the URL** or use the current page
4. **Click "Summarize"** to get AI-powered summary
5. **Ask follow-up questions** for deeper insights

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/summarize` | POST | Summarize article from URL |
| `/ask` | POST | Answer follow-up questions |
| `/session-status` | GET | Get usage statistics |


```

### Usage Limits
- **1 summary** per session
- **2 follow-up questions** per session
- Sessions reset when extension is reopened

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Chrome        │    │   Flask         │    │   Google        │
│   Extension     │◄──►│   Backend       │◄──►│   Gemini AI     │
│   (React)       │    │   (Python)      │    │   API           │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   SQLite3       │
                       │   Database      │
                       └─────────────────┘
```


## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd extension
npm test
```

## 📈 Performance

- **Article Extraction**: < 5 seconds
- **AI Summarization**: < 10 seconds
- **Q&A Response**: < 8 seconds
- **Memory Usage**: < 50MB
- **Database Size**: < 10MB typical

## 🚀 Deployment

### Backend Deployment (Heroku)
```bash
# Create Procfile
echo "web: python app.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Extension Distribution
1. Build: `npm run build`
2. Zip `dist` folder
3. Submit to Chrome Web Store

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push branch: `git push origin feature-name`
5. Submit pull request


## 👨‍💻 Author

Ntokozo Ngakane
- GitHub: ntokozo-sa(https://github.com/ntokozo-sa)
- LinkedIn: Ntokozo Ngakane(https://linkedin.com/in/yourprofile)


## 🙏 Acknowledgments

- Google Gemini AI for powerful language processing
- Chrome Extension API for browser integration
- React team for the excellent UI framework
- Flask community for the lightweight web framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ntokozo-sa/ai-article-summarizer/issues)
- **Email**: ntokozobuthelezi205@gmail.com

---

⭐ **Star this repository if you find it helpful!**