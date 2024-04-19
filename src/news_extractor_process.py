from RPA.Robocloud.Items import Items
from RPA.Robocloud.Secrets import Secrets
from config_manager import ConfigManager
from logging_manager import LoggingManager
from browser_automator import BrowserAutomator
from image_downloader import ImageDownloader
from excel_exporter import ExcelExporter
from datetime import datetime, timedelta
import time


class NewsExtractorProcess:
    def __init__(self):
        # self.work_items = Items()
        # self.secrets = Secrets()
        self.config_manager = ConfigManager("config/config.yaml")
        self.logging_manager = LoggingManager("logs/news_extractor.log")
        self.browser_automator = BrowserAutomator(self.logging_manager)
        self.image_downloader = ImageDownloader("output/images", self.logging_manager)
        self.excel_exporter = ExcelExporter(
            "output/extracted_articles.xlsx", self.logging_manager
        )

    def run(self):
        try:
            # config_data = self.work_items.get_input_work_item()
            website_url = self.config_manager.get_config_value("website_url")
            search_phrase = self.config_manager.get_config_value("search_phrase")
            news_category = self.config_manager.get_config_value("news_category")
            num_months = self.config_manager.get_config_value("num_months")

            self.browser_automator.open_website()
            self.browser_automator.go_to_url(website_url)
            self.browser_automator.enter_search_phrase(search_phrase)
            self.browser_automator.find_article_elements()
            article_count = self.browser_automator.count_article_results()
            print(f"Found {article_count} articles")
            time.sleep(2)

            articles = []
            for i in range(1, article_count+1):
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
        current_date = datetime.now()
        past_date = current_date - timedelta(days=num_months * 30)
        return article_date >= past_date

    def download_article_image(self, article):
        image_url = article.image_url
        filename = f"{article.title.replace(' ', '_')}_{article.date.strftime('%Y-%m-%d')}.jpg"
        return self.image_downloader.download_image(image_url, filename)


if __name__ == "__main__":
    news_extractor = NewsExtractorProcess()
    news_extractor.run()
 