import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-default-secret-key'
    SESSION_COOKIE_NAME = 'your_session_cookie'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or '1234'
    # Add other common configurations here

class DevelopmentConfig(Config):
    DEBUG = True
    # Add development-specific configurations here

class TestingConfig(Config):
    DEBUG = True
    # Add testing-specific configurations here

class ProductionConfig(Config):
    DEBUG = False
    # Add production-specific configurations here

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


