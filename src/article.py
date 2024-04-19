from dataclasses import dataclass
from datetime import datetime
import re

@dataclass
class Article:
    """
    A class representing an article with various attributes and methods.

    Attributes:
        title (str): The title of the article.
        date (datetime): The date of the article.
        description (str): The description or content of the article.
        image_url (str): The URL of the image associated with the article.
        search_phrase_count (int): The count of occurrences of the search phrase in the title and description (default is 0).
        contains_money (bool): A flag indicating whether the article contains money-related information (default is False).
    """

    title: str
    date: datetime
    description: str
    image_url: str
    search_phrase_count: int = 0
    contains_money: bool = False

    def update_search_phrase_count(self, search_phrase: str) -> None:
        """
        Updates the search_phrase_count attribute by counting the number of occurrences of the search phrase in the title and description.

        Args:
            search_phrase (str): The search phrase to count occurrences for.
        """
        self.search_phrase_count = (
            self.title + self.description
        ).lower().count(search_phrase.lower())

    def update_contains_money(self) -> None:
        """
        Updates the contains_money attribute by searching for money-related patterns in the title and description.
        """
        money_regex = r"(\$\d+(\.\d{1,2})?)|(\d+\s+dollars)"
        self.contains_money = bool(
            re.search(money_regex, self.title + self.description, re.IGNORECASE)
        )