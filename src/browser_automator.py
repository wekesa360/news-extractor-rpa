from RPA.Browser.Selenium import Selenium


class BrowserAutomator:
    def __init__(self, logging_manager):
        self.browser = Selenium()
        self.logging_manager = logging_manager

    
    def open_website(self, url):
        try:
            self.browser.open_available_browser(url)
            self.maximize_browser_window()
        except Exception as e:
            self.logging_manager.log_error(f'Error opening website: {str(e)}')
        
    def enter_search_phrase(self, search_phrase):
        try:
            pass
        except Exception as e:
            self.logging_manager.log_error(f'Error entering search phrase: {str(e)}')
    

    def select_news_category(self, category):
        try:
            pass
        except Exception as e:
            self.logging_manager.log_error(f'Error selecting news category: {str(e)}')
    

    def find_article_elements(self):
        try:
            return self.browser.find_elements('css:.article')
        except Exception as e:
            self.logging_manager.log_error(f'Error finding article elements: {str(e)}')
            return []
    
    def close_browser(self):
        try:
            self.browser.close_browser()
        except Exception as e:
            self.logging_manager.log_error(f'Error closing browser: {str(e)}')