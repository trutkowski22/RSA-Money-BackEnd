import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database configuration
    DB_CONFIG = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'pool_size': 20,
        'pool_recycle': 3600
    }
    
    # API Configuration
    API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')
    API_BASE_URL = 'https://www.alphavantage.co/query'
    RATE_LIMIT = 75  # Calls per minute
    
    # Logging Configuration
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Processing Configuration
    BATCH_SIZE = 100
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds
