"""Реализация паттерна Адаптер. Целевой класс Matcher."""
from abc import ABC
from typing import List
from digital_address_matcher.common.types import OutputAddressPart

class AbstractMatcher(ABC):
    """Класс матчер."""
    
    def match(self, addresses: List[str]) -> List[List[OutputAddressPart]]:
        """Сматчить адррес."""
