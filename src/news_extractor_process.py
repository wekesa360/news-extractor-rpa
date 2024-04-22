from robocorp import workitems
from .config_manager import ConfigManager
from .logging_manager import LoggingManager
from .browser_automator import BrowserAutomator
from .image_downloader import ImageDownloader
from .excel_exporter import ExcelExporter
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time

# Reads:  C_WORKITEM_INPUT_PATH=./rc_work_item_test_input.json for workitems testing
# load_dotenv()

class NewsExtractorProcess:
    def __init__(self):
        self.work_items = workitems.inputs.current
        self.logging_manager = LoggingManager("output/news_extractor.log")
        self.browser_automator = BrowserAutomator(self.logging_manager)
        self.config_manager = ConfigManager("./config.yaml", self.logging_manager)
        self.image_downloader = ImageDownloader("output/", self.logging_manager)
        self.excel_exporter = ExcelExporter(
            "output/extracted_articles.xlsx", self.logging_manager
        )


    def run_news_extractor(self):
        """
        Executes the news extraction process.

        This method performs the following steps:
        1. Retrieves the configuration values for website URL, search phrase, news category, and number of months.
        2. Opens the website using the browser automator.
        3. Navigates to the specified URL.
        4. Enters the search phrase into the search field.
        5. Finds the elements containing the articles.
        6. Counts the number of articles found.
        7. Iterates over each article and extracts its data.
        8. Filters the articles based on the news category and date range.
        9. Updates the search phrase count and checks if the article contains money.
        10. Downloads the article image.
        11. Writes the extracted article data to an Excel file.
        12. Closes the browser.

        If any error occurs during the process, it is logged and the browser is closed.

        Returns:
            None
        """
        try:
            try:
                item = workitems.inputs.current
                website_url = item.payload.get("website_url")
                search_phrase = item.payload.get("search_phrase")
                news_category = item.payload.get("news_category")
                num_months = item.payload.get("num_months")
            except Exception as e:
                self.logging_manager.log_info(f"Falling back to config values due to: {str(e)}")
                website_url = self.config_manager.get_config_value("website_url")
                search_phrase = self.config_manager.get_config_value("search_phrase")
                news_category = self.config_manager.get_config_value("news_category")
                num_months = self.config_manager.get_config_value("num_months")

            self.browser_automator.open_website()
            self.browser_automator.go_to_url(website_url)
            self.browser_automator.enter_search_phrase(search_phrase)
            self.browser_automator.find_article_elements()
            article_count = self.browser_automator.count_article_results()
            self.logging_manager.log_info(f"Found {article_count} articles")
            time.sleep(2)

            articles = []
            for i in range(1, article_count + 1):
                if self.browser_automator.check_news_category(news_category, i):
                    article = self.browser_automator.extract_article_data(i)
                    if article and self.is_article_within_date_range(
                        article.date, num_months
                    ):
                        article.update_search_phrase_count(search_phrase)
                        article.update_contains_money()
                        image_url = self.download_article_image(article)
                        article.image_url = image_url
                        articles.append(article)
                else:
                    self.logging_manager.log_warning(
                        f"Skipping article {i} because it is not in the selected category"
                    )
            self.excel_exporter.write_headers(
                [
                    "Title",
                    "Date",
                    "Description",
                    "Image Filename",
                    "Search Phrase Count",
                    "Contains Money",
                ]
            )
            for article in articles:
                row_data = [
                    article.title,
                    article.date.strftime("%Y-%m-%d"),
                    article.description,
                    article.image_url,
                    article.search_phrase_count,
                    article.contains_money,
                ]
                try:
                    self.excel_exporter.write_row(row_data)
                except Exception as e:
                    self.logging_manager.log_error(
                        f"Error writing row to Excel: {str(e)}"
                    )
            self.excel_exporter.save_workbook()

            # self.work_items.create_output_work_item({"extracted_articles": "output/extracted_articles.xlsx"})
            self.logging_manager.log_info(
                "News extraction process completed successfully"
            )
        except Exception as e:
            self.logging_manager.log_error(
                f"Error running news extraction process: {str(e)}"
            )
        finally:
            self.browser_automator.close_browser()

    def is_article_within_date_range(self, article_date, num_months):
        """
        Checks if the article's date is within the 
        specified number of months from the current date.

        Args:
            article_date (datetime): The date of the article.
            num_months (int): The number of months to check against.

        Returns:
            bool: True if the article's date is within 
            the specified number of months, False otherwise.
        """
        current_date = datetime.now()
        past_date = current_date - timedelta(days=num_months * 30)
        return article_date >= past_date

    def download_article_image(self, article):
        """
        Downloads the image for the given article and returns the filename.

        Args:
            article (Article): The article object containing the image URL.

        Returns:
            str: The filename of the downloaded image, 
            or an empty string if an error occurred.
        """
        image_url = article.image_url
        filename = f"""{article.title.replace(' ', '_')
        .replace('.','').replace('?', '').lower()}_{article.date.strftime('%Y-%m-%d')}.jpg"""
        return self.image_downloader.download_image(image_url, filename)