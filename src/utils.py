def covert_cookies_from_header_string_to_json(raw_cookies):
    cookies = []
    for item in raw_cookies.split(";"):
        item = item.strip()
        if "=" not in item:
            continue
        name, value = item.split("=", 1)
        cookies.append({
            "name": name,
            "value": value,
            "domain": ".facebook.com",
            "path": "/"
        })
    return cookies


def check_cookies_missing_value(cookies):
    required = {"c_user", "xs"}
    names = {c["name"] for c in cookies}
    missing = required - names
    print("Missing cookies:", missing)
