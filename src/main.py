import pandas as pd

from selenium import webdriver
import undetected_chromedriver as uc
from contextlib import contextmanager

from navigator import (
    login_with_cookies,
    go_to_groups_page,
)
from scraper import scrape_group_info
from utils import (
    covert_cookies_from_header_string_to_json,
    check_cookies_missing_value,
)


# Config Chrome version
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--start-maximized')


@contextmanager
def get_driver():
    driver = webdriver.Chrome(options=options, version_main=137)
    try:
        yield driver
    finally:
        if driver.service.process and driver.service.process.poll() is None:
            driver.quit()


def save_to_excel(data, output_file):
    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(data)

    # Write DataFrame to an Excel file
    df.to_excel(f'../out/{output_file}.xlsx', index=False, engine='openpyxl')
    print(f"Data saved to {output_file}.xlsx")


group_data = []


def main():
    try:
        with get_driver() as driver:
            # Login Facebook with cookies
            raw_cookies = input('Enter your cookies for login: ')
            cookies = covert_cookies_from_header_string_to_json(raw_cookies)
            check_cookies_missing_value(cookies)
            login_with_cookies(driver, cookies)

            if 'login' in driver.current_url or 'checkpoint' in driver.current_url:
                print('ERROR::Login Failed!')
                return  # Exit if login failed

            print('MESSAGE::Login Successful!')

            search_query = input('Enter Key Search: ')
            go_to_groups_page(driver, search_query)

            number_group = int(input("Enter number group you want scraping: "))
            group_data = scrape_group_info(driver, limit=number_group)
            print(f'MESSAGE:: GROUP DATA: {len(group_data)}')

            # Save group data to an Excel file
            output_file = input('Enter output file name: ')
            save_to_excel(group_data, output_file)

    except Exception as e:
        print(f"ERROR:: An error occurred during scraping: {e}")


if __name__ == '__main__':
    main()
