from RPA.Browser.Selenium import Selenium


class BrowserAutomator:
    def __init__(self, logging_manager):
        self.browser = Selenium()
        self.logging_manager = logging_manager

    
    def open_website(self, url):
        try:
            self.browser.open_available_browser(url, maximized=True)
            # self.maximize_browser_window()
        except Exception as e:
            self.logging_manager.log_error(f'Error opening website: {str(e)}')
        
    def enter_search_phrase(self, search_phrase):
        try:
            # Click the search icon
            search_icon = self.browser.find_element("css:.icon.icon--search.icon--grey.icon--24")
            search_icon.click()

            # Find and interact with the search bar
            search_bar = self.browser.find_element("css:.search-bar__input")
            search_bar.send_keys(search_phrase)
            search_bar.submit()

            # Wait for the search results to appear
            self.browser.wait_until_page_contains_element('css:.search-result__list', timeout=15)
        except Exception as e:
            self.logging_manager.log_error(f'Error entering search phrase: {str(e)}')
    

    def select_news_category(self, category):
        try:
            category_items = self.browser.find_elements('css:.menu_item.menu_item-aje')
            category_found = False
            print(category_items)
            for item in category_items:
                if item.text.lower() == category.lower():
                    item.click()
                    category_found = True
                    break
            if not category_found:
                raise ValueError(f"Category '{category}' not found in the list.")
        except Exception as e:
            self.logging_manager.log_error(f'Error selecting news category: {str(e)}')
    
    def find_article_links(self):
        try:
            article_links = self.browser.find_elements('css:article a.gc_clickable-card_link')
            return [link.get_attribute('href') for link in article_links]
        except Exception as e:
            self.logging_manager.log_error(f'Error finding article links: {str(e)}')
            return []

    def open_article(self, link):
        try:
            self.browser.go_to(link)
            self.browser.wait_until_page_contains_element('#main-content-area')
        except Exception as e:
            self.logging_manager.log_error(f'Error opening article: {str(e)}')

        
    def find_article_element(self):
        try:
            return self.browser.find_element_by_css_selector('#main-content-area')
        except Exception as e:
            self.logging_manager.log_error(f'Error finding article elements: {str(e)}')
            return None
        
    def go_back(self):
        try:
            self.browser.go_back()
            self.browser.wait_until_page_contains_element('css:article.gc-u-clickable-card')
        except Exception as e:
            self.logging_manager.log_error(f'Error going back: {str(e)}')

    def close_browser(self):
        try:
            self.browser.close_browser()
        except Exception as e:
            self.logging_manager.log_error(f'Error closing browser: {str(e)}')