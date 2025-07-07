import time

import undetected_chromedriver as uc

from config import COOKIES

# Config Chrome version\
options = uc.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--start-maximized')
driver = uc.Chrome(options=options, version_main=137)


def login_with_cookies(driver):
    driver.get("https://www.facebook.com")
    time.sleep(2)

    for cookie in COOKIES:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"ERROR::Error when add cookie name: {cookie['name']}", e)

    driver.refresh()
    time.sleep(5)
    print(f"Current URL: {driver.current_url}")


def main(driver):
    login_with_cookies(driver)
    if "login" in driver.current_url or "checkpoint" in driver.current_url:
        print("ERROR::Login Failed!")
    else:
        print("MESSAGE::Login Successful!")


if __name__ == '__main__':
    main(driver)
    driver.quit()
