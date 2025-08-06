import React, { useState, useEffect } from 'react';

// Backend API URL
const BACKEND_URL = 'http://localhost:5000';

function App() {
  // State management
  const [url, setUrl] = useState('');
  const [summary, setSummary] = useState('');
  const [title, setTitle] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Q&A state
  const [questions, setQuestions] = useState(['', '']);
  const [answers, setAnswers] = useState(['', '']);
  const [qaLoading, setQaLoading] = useState([false, false]);
  
  // Session management
  const [sessionId, setSessionId] = useState('');
  const [sessionStatus, setSessionStatus] = useState({
    summary_count: 0,
    qa_count: 0,
    max_summary: 1,
    max_qa: 2
  });

  // Initialize session on component mount
  useEffect(() => {
    initializeSession();
  }, []);

  const initializeSession = () => {
    // Generate or retrieve session ID from localStorage
    let storedSessionId = localStorage.getItem('ai_summarizer_session_id');
    if (!storedSessionId) {
      storedSessionId = generateSessionId();
      localStorage.setItem('ai_summarizer_session_id', storedSessionId);
    }
    setSessionId(storedSessionId);
    
    // Get session status
    fetchSessionStatus(storedSessionId);
  };

  const generateSessionId = () => {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  };

  const fetchSessionStatus = async (sessionId) => {
    try {
      const response = await fetch(`${BACKEND_URL}/session-status?session_id=${sessionId}`);
      if (response.ok) {
        const data = await response.json();
        setSessionStatus(data);
      }
    } catch (error) {
      console.error('Error fetching session status:', error);
    }
  };

  const handleSummarize = async () => {
    if (!url.trim()) {
      setError('Please enter a valid URL');
      return;
    }

    if (sessionStatus.summary_count >= sessionStatus.max_summary) {
      setError('Summary limit reached for this session');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch(`${BACKEND_URL}/summarize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url.trim(),
          session_id: sessionId
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setSummary(data.summary);
        setTitle(data.title);
        setSuccess(data.cached ? 'Summary loaded from cache' : 'Article summarized successfully!');
        
        // Update session status
        await fetchSessionStatus(sessionId);
      } else {
        setError(data.error || 'Failed to summarize article');
      }
    } catch (error) {
      setError('Network error. Please check if the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleAskQuestion = async (index) => {
    const question = questions[index].trim();
    
    if (!question) {
      setError('Please enter a question');
      return;
    }

    if (!summary) {
      setError('Please summarize an article first');
      return;
    }

    if (sessionStatus.qa_count >= sessionStatus.max_qa) {
      setError('Q&A limit reached for this session');
      return;
    }

    // Update loading state for specific question
    const newQaLoading = [...qaLoading];
    newQaLoading[index] = true;
    setQaLoading(newQaLoading);
    setError('');

    try {
      const response = await fetch(`${BACKEND_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question,
          url: url,
          session_id: sessionId
        }),
      });

      const data = await response.json();

      if (response.ok) {
        const newAnswers = [...answers];
        newAnswers[index] = data.answer;
        setAnswers(newAnswers);
        
        // Update session status
        await fetchSessionStatus(sessionId);
      } else {
        setError(data.error || 'Failed to get answer');
      }
    } catch (error) {
      setError('Network error. Please check if the backend server is running.');
    } finally {
      const newQaLoading = [...qaLoading];
      newQaLoading[index] = false;
      setQaLoading(newQaLoading);
    }
  };

  const handleQuestionChange = (index, value) => {
    const newQuestions = [...questions];
    newQuestions[index] = value;
    setQuestions(newQuestions);
  };

  const resetSession = () => {
    localStorage.removeItem('ai_summarizer_session_id');
    setSummary('');
    setTitle('');
    setQuestions(['', '']);
    setAnswers(['', '']);
    setError('');
    setSuccess('');
    initializeSession();
  };

  const canSummarize = sessionStatus.summary_count < sessionStatus.max_summary;
  const canAskQuestions = sessionStatus.qa_count < sessionStatus.max_qa;

  return (
    <div className="container">
      {/* Header */}
      <div className="header">
        <h1>AI Article Summarizer</h1>
        <p>Powered by Google Gemini</p>
      </div>

      {/* Main Content */}
      <div className="content">
        {/* Session Status */}
        <div className="status">
          <div className="status-item">
            <span>Summaries:</span>
            <span className="status-count">{sessionStatus.summary_count}/{sessionStatus.max_summary}</span>
          </div>
          <div className="status-item">
            <span>Q&A:</span>
            <span className="status-count">{sessionStatus.qa_count}/{sessionStatus.max_qa}</span>
          </div>
        </div>

        {/* Error/Success Messages */}
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}

        {/* URL Input */}
        <div className="form-group">
          <label htmlFor="url">Article URL</label>
          <input
            type="url"
            id="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com/article"
            disabled={!canSummarize}
          />
        </div>

        {/* Summarize Button */}
        <div className="text-center mb-16">
          <button
            className="btn btn-primary"
            onClick={handleSummarize}
            disabled={loading || !canSummarize}
          >
            {loading && <span className="loading"></span>}
            {loading ? 'Summarizing...' : 'Summarize Article'}
          </button>
        </div>

        {/* Summary Results */}
        {summary && (
          <div className="results">
            <div className="result-card">
              <h3>{title}</h3>
              <p>{summary}</p>
            </div>
          </div>
        )}

        {/* Q&A Section */}
        {summary && (
          <div className="qa-section">
            <h3>Ask Follow-up Questions</h3>
            
            {[0, 1].map((index) => (
              <div key={index} className="qa-item">
                <div className="form-group">
                  <label htmlFor={`question-${index}`}>Question {index + 1}</label>
                  <textarea
                    id={`question-${index}`}
                    value={questions[index]}
                    onChange={(e) => handleQuestionChange(index, e.target.value)}
                    placeholder="Ask a question about the article..."
                    disabled={!canAskQuestions || qaLoading[index]}
                  />
                </div>
                
                <div className="text-center">
                  <button
                    className="btn btn-secondary"
                    onClick={() => handleAskQuestion(index)}
                    disabled={!canAskQuestions || qaLoading[index] || !questions[index].trim()}
                  >
                    {qaLoading[index] && <span className="loading"></span>}
                    {qaLoading[index] ? 'Getting Answer...' : 'Ask Question'}
                  </button>
                </div>

                {answers[index] && (
                  <div className="mt-16">
                    <div className="qa-question">Q: {questions[index]}</div>
                    <div className="qa-answer">A: {answers[index]}</div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Reset Session Button */}
        <div className="text-center mt-16">
          <button
            className="btn btn-secondary"
            onClick={resetSession}
          >
            Reset Session
          </button>
        </div>
      </div>
    </div>
  );
}

export default App; 