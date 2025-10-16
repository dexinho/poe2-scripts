import time
from utility.errors import PoeNotActiveError


def wait_for(callback, *args, wait_threshold=100, delay=0.1):
    for attempt in range(wait_threshold):
        if callback(*args):
            return True
        time.sleep(delay)
    raise PoeNotActiveError(f"Timeout waiting for {callback.__name__}")
