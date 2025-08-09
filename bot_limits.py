import datetime
import logging
import os

from dotenv import load_dotenv

last_request_date = datetime.date.today()
num_requests = 0

load_dotenv()
logger = logging.getLogger(__name__)

MAX_DAILY_REQUESTS = os.environ.get("MAX_DAILY_REQUESTS", 100)

def increment_limit(inc: int = 1) -> bool:
    """
    Increments the number of requests by `inc` and checks if the usage is
    still within the limit
    :return: True if the limit is not exceeded and False, otherwise
    """
    global last_request_date
    global num_requests
    today = datetime.date.today()
    if last_request_date < today:
        logger.info("Resetting usage limit")
        last_request_date = today
        num_requests = 0
    num_requests += inc
    return num_requests <= MAX_DAILY_REQUESTS
