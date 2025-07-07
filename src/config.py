import os
import json

from dotenv import load_dotenv

load_dotenv()  # take environment variables

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.

# Load cookies from .env
RAW_COOKIES = os.getenv('COOKIES')
COOKIES = []
for item in RAW_COOKIES.split(";"):
    item = item.strip()
    if "=" not in item:
        continue
    name, value = item.split("=", 1)
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
