import os

class Config:
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'lifeline-hospital-dev-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///lifeline_hospital.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_TRANSLATION_DIRECTORIES = 'translations'
    LANGUAGES = {
        'en': 'English',
        'hi': 'Hindi',
        'ur': 'Urdu'
    }
    UPLOADS_DEFAULT_DEST = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    HIPAA_COMPLIANT = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600  # 1 hour
