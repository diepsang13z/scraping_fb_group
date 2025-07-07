import os
import json

from dotenv import load_dotenv

load_dotenv()  # take environment variables

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.

# Load cookies from .env
RAW_COOKIES = json.loads(os.getenv('COOKIES'))
COOKIES = []
for name, value in RAW_COOKIES.items():
    COOKIES.append({
        "name": name,
        "value": value,
        "domain": ".facebook.com",
        "path": "/"
    })

# Check valid cookies
required = {"c_user", "xs"}
names = {c["name"] for c in COOKIES}
missing = required - names
print("Missing cookies:", missing)
