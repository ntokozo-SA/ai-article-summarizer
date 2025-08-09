import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise RuntimeError('GEMINI_API_KEY is not set. Create backend/.env and set GEMINI_API_KEY.')

# Flask Configuration
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this')

# Database Configuration
DATABASE_PATH = 'usage_tracker.db'

# API Configuration
MAX_SUMMARY_PER_SESSION = 1
MAX_QA_PER_SESSION = 2

# CORS Configuration
ALLOWED_ORIGINS = [
    'chrome-extension://*',
    'http://localhost:3000',
    'http://localhost:5000'
] 