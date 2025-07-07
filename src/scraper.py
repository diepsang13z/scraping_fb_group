import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_group_info(driver, limit=10):
    groups_data = []

    current_scroll_position = 0
    scroll_increment = 300

    visited_links = set()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@role='feed']//div[@role='article']")
            )
        )

        while len(groups_data) < limit:
            # Scroll
            driver.execute_script(
                f"window.scrollTo(0, {current_scroll_position});")

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[@role='feed']//div[@role='article']")
                )
            )

            current_scroll_position += scroll_increment  # Update page position

            # Scraping all group available in HTML
            group_elements = driver.find_elements(
                By.XPATH, "//div[@role='feed']//div[@role='article']"
            )

            if not group_elements:
                print("No groups found on the page.")
                break

            for group in group_elements:
                try:
                    # Collect group name
                    group_name_element = group.find_element(
                        By.XPATH, './/a[contains(@href, "facebook.com/groups") and text() != ""]'
                    )
                    group_name = group_name_element.text if group_name_element else "No name"

                    # Collect group link
                    group_link = group_name_element.get_attribute(
                        "href") if group_name_element else "No link"

                    if group_link in visited_links:
                        continue

                    # Collect group member count
                    member_count_element = group.find_element(
                        By.XPATH, './/span[contains(text(), "members")]'
                    )
                    members = member_count_element.text if member_count_element else "No members"

                    collected_data = {
                        'name': group_name,
                        'link': group_link,
                        'members': members
                    }
                    groups_data.append(collected_data)
                    print(f'Collected Data:: {collected_data}')

                    visited_links.add(group_link)

                    if len(groups_data) >= limit:
                        break
                except Exception as e:
                    print(f"Error extracting data for a group: {e}")

            if len(groups_data) >= limit:
                break

    except Exception as e:
        print(f"ERROR::Failed to scrape group info: {e}")

    return groups_data
