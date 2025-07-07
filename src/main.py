import undetected_chromedriver as uc

from navigator import (
    login_with_cookies,
    search_and_get_query,
    go_to_groups_page,
)

from scraper import scrape_group_info

# Config Chrome version\
options = uc.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--start-maximized')
driver = uc.Chrome(options=options, version_main=137)

group_data = []


def main(driver):
    try:
        login_with_cookies(driver)

        if 'login' in driver.current_url or 'checkpoint' in driver.current_url:
            print('ERROR::Login Failed!')
            return  # Exit if login failed

        print('MESSAGE::Login Successful!')

        search_query = "Tài liệu Ielts"
        search_query_from_url = search_and_get_query(driver, search_query)

        if search_query_from_url:
            go_to_groups_page(driver, search_query_from_url)
        else:
            print("ERROR::Could not extract search query, skipping group navigation.")

        group_data = scrape_group_info(driver, limit=50)
        print(f'MESSAGE:: GROUP DATA: {len(group_data)}')

    except Exception as e:
        print(f"ERROR:: An error occurred during scraping: {e}")

    finally:
        try:
            # Check if driver is still active and quit it properly
            if driver.service.process and driver.service.process.poll() is None:
                driver.quit()
            else:
                print("ERROR:: WebDriver process is not running.")
        except Exception as e:
            print(f"ERROR:: Failed to quit the driver properly: {e}")


if __name__ == '__main__':
    main(driver)
