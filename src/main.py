import undetected_chromedriver as uc

from navigator import (
    login_with_cookies,
    search_and_get_query,
    go_to_groups_page,
)

# Config Chrome version\
options = uc.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--start-maximized')
driver = uc.Chrome(options=options, version_main=137)


def main(driver):
    login_with_cookies(driver)

    if 'login' in driver.current_url or 'checkpoint' in driver.current_url:
        print('ERROR::Login Failed!')

    print('MESSAGE::Login Successful!')

    search_query = "Tài liệu Ielts"
    search_query_from_url = search_and_get_query(driver, search_query)

    if search_query_from_url:
        go_to_groups_page(driver, search_query_from_url)
    else:
        print("ERROR::Could not extract search query, skipping group navigation.")


if __name__ == '__main__':
    main(driver)
    driver.quit()
