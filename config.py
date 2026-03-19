import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG') or 0
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/uploads')
    TESTING = 0
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    PASSWORD_HASH = os.environ.get('PASSWORD_HASH') or 'pbkdf2:sha256:600000$zc8tNa0LofcsJ0HF$2ffeaa047f6e24c2e4995ddbde44ab4b2355d46127e3db83d23c0c977e56f9e0'
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD') or 'AdminTest2025'
    DATABASE_USER = os.environ.get('DATABASE_USER') or 'westonloop_ossian'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@localhost:3306/westonloop_dashboard'
    SQLALCHEMY_ECHO = 'debug'
    
    SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_recycle": 280,
    "pool_pre_ping": True,
    }
    RAW_CSV_FOLDER = os.path.join(basedir,'app/datasets/raw')
    PROCESSED_CSV_FOLDER = os.path.join(basedir,'app/datasets/processed')
