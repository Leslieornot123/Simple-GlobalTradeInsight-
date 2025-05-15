import time
import psutil
import logging
from functools import wraps
import numpy as np
from typing import Callable, Any

class PerformanceMonitor:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('PerformanceMonitor')
        
    def measure_performance(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.perf_counter()
            start_memory = psutil.Process().memory_info().rss
            
            result = func(*args, **kwargs)
            
            end_time = time.perf_counter()
            end_memory = psutil.Process().memory_info().rss
            
            execution_time = end_time - start_time
            memory_used = (end_memory - start_memory) / 1024 / 1024  # Convert to MB
            
            self.logger.info(f"Function {func.__name__} took {execution_time:.4f} seconds and used {memory_used:.2f} MB of memory")
            return result
        return wrapper

    def profile_memory(self):
        process = psutil.Process()
        memory_info = process.memory_info()
        self.logger.info(f"Current memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")

# Global instance
monitor = PerformanceMonitor() 