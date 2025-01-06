import time
import requests
from typing import List, Dict
from src.config.settings import Config
from src.utils.logger import logger

class APIRunner:
    def __init__(self):
        self.last_call_time = 0
        self.call_count = 0
        
    def make_api_call(self, function: str, params: Dict = None) -> Dict:
        """Make API call with rate limiting"""
        self._enforce_rate_limit()
        
        params = params or {}
        params.update({
            'function': function,
            'apikey': Config.API_KEY
        })
        
        try:
            response = requests.get(Config.API_BASE_URL, params=params)
            response.raise_for_status()
            self.call_count += 1
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API call failed: {e}")
            raise

    def _enforce_rate_limit(self):
        """Enforce rate limit of 75 calls per minute"""
        current_time = time.time()
        time_since_last_call = current_time - self.last_call_time
        
        if self.call_count >= Config.RATE_LIMIT:
            if time_since_last_call < 60:
                sleep_time = 60 - time_since_last_call
                logger.info(f"Rate limit reached. Sleeping for {sleep_time} seconds")
                time.sleep(sleep_time)
                self.call_count = 0
                self.last_call_time = time.time()
            else:
                self.call_count = 0
                self.last_call_time = time.time()
