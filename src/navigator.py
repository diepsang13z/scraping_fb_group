import time
from urllib.parse import urlparse, parse_qs

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import COOKIES


def login_with_cookies(driver):
    driver.get('https://www.facebook.com')
    time.sleep(2)

    for cookie in COOKIES:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f'ERROR::Error when add cookie name: {cookie['name']}', e)

    driver.refresh()
    time.sleep(5)
    print(f"Current URL: {driver.current_url}")


def search_and_get_query(driver, search_query):
    try:
        # Wait until the search input is visible and search
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@placeholder="Search Facebook"]'))
        )
        search_box.send_keys(search_query)  # Enter the search query
        search_box.send_keys(Keys.RETURN)  # Press Enter to search
        time.sleep(3)  # Wait for the results to load
        print(f'Search completed for: {search_query}')

        # Get the current URL and extract the search query (q)
        current_url = driver.current_url
        parsed_url = urlparse(current_url)
        query_params = parse_qs(parsed_url.query)

        # Get the value of 'q' from the URL if it exists
        if 'q' in query_params:
            search_query_from_url = query_params['q'][0]
            print(f"Extracted search query from URL: {search_query_from_url}")
            return search_query_from_url
        else:
            print("ERROR::No search query found in URL.")
            return None
    except Exception as e:
        print(f'ERROR::Failed during search or URL extraction: {e}')
        return None


def go_to_groups_page(driver, search_query):
    if search_query:
        # Construct the new URL for groups search
        groups_url = f"https://www.facebook.com/search/groups?q={search_query}"

        # Navigate to the groups search page
        driver.get(groups_url)
        time.sleep(5)
        print(f"Navigated to: {groups_url}")
    else:
        print("ERROR::Search query is empty, cannot navigate to groups page.")
