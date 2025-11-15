import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret')

    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', '../database/library.db')

    # Fine Settings
    FINE_PER_DAY = float(os.getenv('FINE_PER_DAY', 5.00))
    MAX_FINE_AMOUNT = float(os.getenv('MAX_FINE_AMOUNT', 500.00))

    # Issue Settings
    MAX_BOOKS_PER_USER = int(os.getenv('MAX_BOOKS_PER_USER', 5))
    DEFAULT_ISSUE_DAYS = int(os.getenv('DEFAULT_ISSUE_DAYS', 14))

    # JWT
    JWT_EXPIRATION_HOURS = 24

    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
