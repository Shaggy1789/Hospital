import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', False)

class DatabaseConfig:
    """Database configuration"""
    HOST = os.getenv('DB_HOST', 'localhost')
    PORT = int(os.getenv('DB_PORT', 3306))
    USER = os.getenv('DB_USER', 'root')
    PASSWORD = os.getenv('DB_PASSWORD', 'Tortadeuwu2/')
    DATABASE = os.getenv('DB_NAME', 'hospital_monitoring')

class ServerConfig:
    """Server configuration"""
    HOST = os.getenv('SERVER_HOST', 'localhost')
    PORT = int(os.getenv('SERVER_PORT', 5000))
