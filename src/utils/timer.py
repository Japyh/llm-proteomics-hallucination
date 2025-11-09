"""Timer utilities for performance measurement."""
import time
from contextlib import contextmanager

@contextmanager
def timer_context(name: str):
    """Context manager for timing code blocks."""
    start = time.time()
    yield
    end = time.time()
    print(f"{name} took {end-start:.2f}s")

class Timer:
    """Simple timer class."""
    def __init__(self):
        self.start_time = None
    
    def start(self):
        self.start_time = time.time()
    
    def stop(self):
        if self.start_time:
            elapsed = time.time() - self.start_time
            self.start_time = None
            return elapsed
        return None
