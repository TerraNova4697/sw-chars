"""
Abstract method for SW data source.
"""

from abc import ABC, abstractmethod


class SWSource(ABC):

    @abstractmethod
    def get_chars(self, key: str):
        pass

    @abstractmethod
    def get_item(self, type: str, key: int):
        pass
