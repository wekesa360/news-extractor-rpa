import re
from datetime import datetime
from article import Article


class ArticleExtractor:
    def __init__(self, logging_manager):
        self.logging_manager = logging_manager

    def extract_article_data(self, article_element):
        try:
            title = article_element.find_element('css:.article-header').text.strip()
            date_string = article_element.find_element('css:.date-simple').text.strip()
            date = self.parse_date(date_string)
            description = article_element.find_element('css:.wysiwyg--all-content').text.strip()
            image_url = article_element.find_element('css:.responsive-image img').get_attribute('src')
            image_url = 'https://www.aljazeera.com' + image_url if not image_url.startswith('/wp-content') else image_url
            return Article(title=title, date=date, description=description, image_url=image_url)
        except Exception as e:
            self.logging_manager.log_error(f'Error extracting article data: {str(e)}')
            return None
    
    @staticmethod
    def parse_date(date_string):
        date_formats = ["%a, %B %d, %Y at %I:%M %p %Z", "%Y-%m-%d", "%m/%d/%Y", "%d %b %Y"]
        for fmt in date_formats:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                pass
        raise ValueError(f"No valid date format found for: {date_string}")
