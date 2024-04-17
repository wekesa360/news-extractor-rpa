from dataclasses import dataclass
from datetime import datetime
import re


@dataclass
class Article:
    title: str
    date: datetime
    description: str
    image_filename: str
    search_phrase_count: int = 0
    contains_money: bool = False

    def update_search_phrase_count(self, search_phrase: str) -> None:
        self.search_phrase_count = (self.title + self.description).lower().count(search_phrase.lower())
    
    def update_contains_money(self) -> None:
        money_regex = r'(\$\d+(\.\d{1,2})?)|(\d+\s+dollars)'
        self.contains_money = bool(re.search(money_regex, self.title + self.description))