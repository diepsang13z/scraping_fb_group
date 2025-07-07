import pandas as pd

import undetected_chromedriver as uc
from contextlib import contextmanager

from navigator import (
    login_with_cookies,
    search_and_get_query,
    go_to_groups_page,
)

from scraper import scrape_group_info

# Config Chrome version
options = uc.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--start-maximized')


@contextmanager
def get_driver():
    driver = uc.Chrome(options=options, version_main=137)
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
            login_with_cookies(driver)

            if 'login' in driver.current_url or 'checkpoint' in driver.current_url:
                print('ERROR::Login Failed!')
                return  # Exit if login failed

            print('MESSAGE::Login Successful!')

            search_query = input('Enter Key Search: ')
            search_query_from_url = search_and_get_query(driver, search_query)
            number_group = int(input("Enter number group you want scraping: "))

            if search_query_from_url:
                go_to_groups_page(driver, search_query_from_url)
            else:
                print(
                    "ERROR::Could not extract search query, skipping group navigation.")

            group_data = scrape_group_info(driver, limit=number_group)
            print(f'MESSAGE:: GROUP DATA: {len(group_data)}')

            # Save group data to an Excel file
            output_file = input('Enter output file name: ')
            save_to_excel(group_data, output_file)

    except Exception as e:
        print(f"ERROR:: An error occurred during scraping: {e}")


if __name__ == '__main__':
    main()
