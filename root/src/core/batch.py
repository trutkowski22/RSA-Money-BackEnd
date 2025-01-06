from typing import List, Dict, Callable
from concurrent.futures import ThreadPoolExecutor
from src.utils.logger import logger

class BatchProcessor:
    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
        
    def process_batch(self, items: List, process_fn: Callable) -> List:
        """Process items in batches"""
        results = []
        total_items = len(items)
        
        for i in range(0, total_items, self.batch_size):
            batch = items[i:i + self.batch_size]
            logger.info(f"Processing batch {i//self.batch_size + 1} of {total_items//self.batch_size + 1}")
            
            with ThreadPoolExecutor() as executor:
                batch_results = list(executor.map(process_fn, batch))
                results.extend(batch_results)
                
        return results
