from joblib import Parallel, delayed
from numba import jit
import numpy as np
from typing import List, Callable, Any
from tqdm import tqdm

class ParallelProcessor:
    def __init__(self, n_jobs: int = -1):
        self.n_jobs = n_jobs  # -1 means use all available cores
        
    def parallel_map(self, func: Callable, items: List[Any], use_tqdm: bool = True) -> List[Any]:
        """Execute function in parallel on a list of items"""
        if use_tqdm:
            return Parallel(n_jobs=self.n_jobs)(
                delayed(func)(item) for item in tqdm(items, desc="Processing")
            )
        return Parallel(n_jobs=self.n_jobs)(delayed(func)(item) for item in items)

    @staticmethod
    @jit(nopython=True)
    def vectorized_operation(data: np.ndarray) -> np.ndarray:
        """Example of a vectorized operation using numba"""
        return np.sqrt(np.sum(data**2, axis=1))

# Global instance
processor = ParallelProcessor() 