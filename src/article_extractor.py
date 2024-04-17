import re
from datetime import datetime
from article import Article


class ArticleExtractor:
    def __init__(self, logging_manager):
        self.logging_manager = logging_manager

    def extract_article_data(self, article_element):
        try:
            title = article_element.find_element_by_css_selector('.title').text
            date = self.parse_date(article_element.find_element_by_css_selector('.date').text)
            description = article_element.find_element_by_css_selector('.description').text
            image_url = article_element.find_element_by_css_selector('img').get_attribute('src')
            return Article(title=title, date=date, description=description, image_filename='')
        except Exception as e:
            self.logging_manager.log_error(f'Error extracting article data: {str(e)}')
            return None
    
    @staticmethod
    def parse_date(date_string):
        return datetime.strptime(date_string, '%B %d, %Y')
