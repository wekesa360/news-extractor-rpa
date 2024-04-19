from RPA.Browser.Selenium import Selenium
from datetime import datetime
from article import Article
import time
import re


class BrowserAutomator:
    def __init__(self, logging_manager):
        self.browser = Selenium()
        self.logging_manager = logging_manager

    def open_website(self):
        """Launches the available browser using the Selenium library."""
        try:
            self.browser.open_available_browser()
        except Exception as e:
            self.logging_manager.log_error(f"Error opening website: {str(e)}")

    def go_to_url(self, url):
        """Navigates to the given URL and maximizes the browser window.

        Args:
            url (str): The URL to navigate to.
        """
        try:
            self.browser.go_to(url)
            self.browser.maximize_browser_window()
        except Exception as e:
            self.logging_manager.log_error(f"Error going to URL: {str(e)}")

    def enter_search_phrase(self, search_phrase):
        """Performs a search by entering the given search phrase 
        in the search bar and clicking the search icon.

        It also waits for the initial search results to 
        appear and loads all available results by clicking the
        "Show More" button until it's no longer present.

        Args:
            search_phrase (str): The search phrase to 
            be entered in the search bar.
        """
        try:
            search_icon = self.browser.find_element(
            '//*[@id="app"]/div[2]/div[2]/header/section[1]/div[1]/div/button'
            )
            search_icon.click()
            time.sleep(1)

            search_bar = self.browser.find_element(
                '//*[@id="search-input"]/form/div/input'
            )
            search_bar.send_keys(search_phrase)
            time.sleep(1)
            search_bar.submit()

            self.browser.wait_until_page_contains_element(
                '//*[@id="site-content"]/div/div[2]/div[2]/ol', timeout=10
            )

            max_iterations = 5 
            iteration_count = 0
            while self.click_show_more_button():
                time.sleep(2)
                iteration_count += 1
                if iteration_count >= max_iterations:
                    self.logging_manager.log_warning(
                        f"""Maximum number of iterations ({max_iterations}) 
                        reached for clicking 'Show More' button."""
                    )
                    break
        except Exception as e:
            self.logging_manager.log_error(
                f"Error entering search phrase: {str(e)}"
                )

    def click_show_more_button(self):
        """Clicks the "Show More" button to load additional search results.

        Returns:
            bool: True if the "Show More" button is clicked, False otherwise.
        """
        try:
            show_more_button = self.browser.find_element(
                'css:button[data-testid="search-show-more-button"]'
            )
            if show_more_button.is_displayed():
                show_more_button.click()
                return True
            else:
                return False
        except Exception as e:
            self.logging_manager.log_error(
                f'Error clicking "Show More" button: {str(e)}'
            )
            return False

    def check_news_category(self, category, article_no):
        """Checks if the specified news category matches 
        the category of the given article number.

        Args:
            category (str): The news category to check.
            article_no (int): The article number (1-based index).

        Returns:
            bool: True if the category matches, False otherwise.
        """
        try:
            # Wait for the article elements to be loaded
            article_xpath = f'//li[@data-testid="search-bodega-result"][{article_no}]'
            self.browser.wait_until_page_contains_element(
                article_xpath, timeout=5
                )

            category_xpath = f"{article_xpath}//div/p"
            category_item = self.browser.find_element(category_xpath)
            category_found = False
            if category_item.text.strip().lower() == category.lower():
                category_found = True
            return category_found

        except Exception as e:
            self.logging_manager.log_error(
                f"Error selecting news category: {str(e)}"
                )
            return False

    def count_article_results(self):
        """Counts the number of article results displayed on the page.

        Returns:
            int: The number of article results.
        """
        try:
            article_items = self.find_article_elements()
            article_count = len(article_items)
            self.logging_manager.log_info(f"Found {article_count} article results.")
            return article_count
        except Exception as e:
            self.logging_manager.log_error(f"Error counting article results: {str(e)}")
            return 0

    def extract_article_data(self, article_no):
        """Extracts the data (title, date, description,
          image URL) for the specified article number.

        Args:
            article_no (int): The article number (1-based index).

        Returns:
            Article: An Article object containing 
            the extracted data, or None if the article doesn't have a title.
        """
        try:
            article_xpath = f'//li[@data-testid="search-bodega-result"][{article_no}]'
            self.browser.wait_until_page_contains_element(article_xpath, timeout=10)

            title_xpath = f"{article_xpath}//div/div/div/a/h4"
            date_xpath = f'{article_xpath}//div/span[@data-testid="todays-date"]'
            description_xpath = f"{article_xpath}//div/div/div/a/p[1]"
            image_xpath = f"{article_xpath}//div/div/figure/div/img"

            if not self.browser.find_elements(title_xpath):
                self.logging_manager.log_warning(
                    f"Skipping article {article_no} as it does not have a title."
                )
                return None

            title = self.browser.find_element(title_xpath).text.strip()
            date_string = (
                self.browser.find_element(date_xpath).text.strip().replace(".", "")
            )
            date = self.parse_date(date_string)
            description = self.browser.find_element(description_xpath).text.strip()

            try:
                image_url = self.browser.find_element(image_xpath).get_attribute("src")
            except Exception:
                image_url = ""

            return Article(
                title=title, date=date, description=description, image_url=image_url
            )
        except Exception as e:
            self.logging_manager.log_error(f"Error extracting article data: {str(e)}")
            return None

    def parse_date(self, date_string):
        """
        Parses a date string and returns a datetime object.

        Args:
            date_string (str): The date string to be parsed.

        Returns:
            datetime: The parsed datetime object.

        Raises:
            ValueError: If no valid date format is found.
        """
        current_year = datetime.now().year
        date_formats = [
            "%B %d, %Y",  # e.g., April 20, 2023
            "%b %d, %Y",  # e.g., Apr 20, 2023
            "%m/%d/%Y",  # e.g., 04/20/2023
            "%d %b %Y",  # e.g., 20 Apr 2023
            "%B %d",  # e.g., April 20
            "%b %d",  # e.g., Apr 20
            "%b %d, %Y",  # e.g., Sept 25, 2023
        ]

        date_string = date_string.strip()

        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_string, fmt)
                if parsed_date.year == 1900:
                    parsed_date = parsed_date.replace(year=current_year)
                return parsed_date
            except ValueError:
                pass

        raise ValueError(f"No valid date format found for: {date_string}")

    def find_article_elements(self):
        """Finds all the article elements on the page.

        Returns:
            list: A list of WebElement objects representing the article elements.
        """
        try:
            self.browser.wait_until_page_contains_element(
                'css:li.css-1l4w6pd[data-testid="search-bodega-result"]', timeout=10
            )
            return self.browser.find_elements(
                'css:li.css-1l4w6pd[data-testid="search-bodega-result"]'
            )
        except Exception as e:
            self.logging_manager.log_error(f"Error finding article elements: {str(e)}")
            return []

    def close_browser(self):
        """Closes the browser."""
        try:
            self.browser.close_browser()
        except Exception as e:
            self.logging_manager.log_error(f"Error closing browser: {str(e)}")
