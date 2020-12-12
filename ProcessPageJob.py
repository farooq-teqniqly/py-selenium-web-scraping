import hashlib
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class ProcessPageJob:
    def __init__(self, uri, driver, db):
        self.driver = driver
        self.db = db
        self.driver.get(uri)

    def run(self, db_start_page: int, root_ratings_url: str, sleep_time: int):

        current_page_num = 1
        current_sleep_time = sleep_time

        while True:
            print(f"Current url: {self.driver.current_url}")

            if current_page_num >= db_start_page:
                current_sleep_time = sleep_time * 2.5
                review_links = self._get_review_links()
                print(f"Found {len(review_links)} reviews.")

                # get urls for ratings on the page
                for (i, link) in enumerate(review_links):
                    href = link.get_attribute("href")
                    relative_ratings_url = href[len(root_ratings_url) : -1]
                    sha = hashlib.sha256(relative_ratings_url.encode()).hexdigest()

                    self.db.execute(
                        f"insert into reviews (page_no, url, sha) values (?, ?, ?)",
                        (current_page_num, relative_ratings_url, sha),
                    )

                    self.db.commit()
                    print(f"Inserted url '{href}' into db.")
            else:
                print(f"Already processed page {current_page_num}.")

            next_page_link = self._get_next_page_link()

            if not next_page_link:
                print("Next page link not found. Exiting.")
                return

            self.driver.execute_script("arguments[0].click();", next_page_link)
            print(f"Going to next page: {next_page_link.text}...")
            next_page_link = self._get_next_page_link()
            current_page_num = int(next_page_link.text)
            time.sleep(current_sleep_time)

    def _read_page(self, link):
        if not link:
            raise ValueError("Link cannot be null.")

        self.driver.execute_script("arguments[0].click();", link)
        time.sleep(1)
        print(f"_read_page():reading {self.driver.current_url}")
        content = self.driver.page_source
        return content

    def _get_review_links(self):
        return self.driver.find_elements_by_css_selector(".review-listing[href]")

    def _get_element_by_css_selector(self, selector: str):
        return WebDriverWait(self.driver, 60).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

    def _get_next_page_link(self):
        next_page_element = self._get_element_by_css_selector("#next-page")
        next_page_number = next_page_element.get_attribute("data-page-number")

        next_page_number_element = self._get_element_by_css_selector(
            f'[data-page-number="{next_page_number}"]'
        )

        return next_page_number_element
