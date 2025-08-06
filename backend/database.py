import sqlite3
import time
from config import DATABASE_PATH

class UsageTracker:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                summary_count INTEGER DEFAULT 0,
                qa_count INTEGER DEFAULT 0,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create articles table to cache article content
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                url TEXT PRIMARY KEY,
                title TEXT,
                content TEXT,
                summary TEXT,
                session_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (session_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_or_create_session(self, session_id):
        """Get existing session or create a new one"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if session exists
        cursor.execute('SELECT * FROM sessions WHERE session_id = ?', (session_id,))
        session = cursor.fetchone()
        
        if not session:
            # Create new session
            cursor.execute('''
                INSERT INTO sessions (session_id, summary_count, qa_count)
                VALUES (?, 0, 0)
            ''', (session_id,))
            conn.commit()
            session = (session_id, time.time(), 0, 0, time.time())
        
        conn.close()
        return {
            'session_id': session[0],
            'created_at': session[1],
            'summary_count': session[2],
            'qa_count': session[3],
            'last_activity': session[4]
        }
    
    def increment_summary_count(self, session_id):
        """Increment summary count for a session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE sessions 
            SET summary_count = summary_count + 1, last_activity = CURRENT_TIMESTAMP
            WHERE session_id = ?
        ''', (session_id,))
        
        conn.commit()
        conn.close()
    
    def increment_qa_count(self, session_id):
        """Increment Q&A count for a session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE sessions 
            SET qa_count = qa_count + 1, last_activity = CURRENT_TIMESTAMP
            WHERE session_id = ?
        ''', (session_id,))
        
        conn.commit()
        conn.close()
    
    def save_article(self, url, title, content, summary, session_id):
        """Save article content and summary to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO articles (url, title, content, summary, session_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (url, title, content, summary, session_id))
        
        conn.commit()
        conn.close()
    
    def get_article(self, url):
        """Get cached article content and summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT title, content, summary FROM articles WHERE url = ?', (url,))
        article = cursor.fetchone()
        
        conn.close()
        
        if article:
            return {
                'title': article[0],
                'content': article[1],
                'summary': article[2]
            }
        return None
    
    def cleanup_old_sessions(self, max_age_hours=24):
        """Clean up sessions older than specified hours"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete old sessions and their associated articles
        cursor.execute('''
            DELETE FROM articles 
            WHERE session_id IN (
                SELECT session_id FROM sessions 
                WHERE last_activity < datetime('now', '-{} hours')
            )
        '''.format(max_age_hours))
        
        cursor.execute('''
            DELETE FROM sessions 
            WHERE last_activity < datetime('now', '-{} hours')
        '''.format(max_age_hours))
        
        conn.commit()
        conn.close() 