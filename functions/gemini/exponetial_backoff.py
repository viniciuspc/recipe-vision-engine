import random
import time
from google.genai.errors import ServerError

BASE_DELAY = 30      # seconds
CAP = 300            # seconds
MAX_RETRIES = 5

def exponential_backoff_with_full_jitter(attempt):
    max_delay = min(CAP, BASE_DELAY * (2 ** (attempt - 1)))
    return random.uniform(0, max_delay)

def call_with_retry(fn, args):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return fn(**args)
        except ServerError as e:
            if attempt == MAX_RETRIES or e.code != 503:
                raise
            wait = exponential_backoff_with_full_jitter(attempt)
            print(f"retry {attempt}, waiting {wait:.2f}s")
            time.sleep(wait)
