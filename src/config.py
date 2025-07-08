import os

from dotenv import load_dotenv

from utils import (
    covert_cookies_from_header_string_to_json,
    check_cookies_missing_value,
)

load_dotenv()  # take environment variables

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.

# Load cookies from .env
RAW_COOKIES = os.getenv('COOKIES')
COOKIES = covert_cookies_from_header_string_to_json(RAW_COOKIES)
check_cookies_missing_value(COOKIES)
