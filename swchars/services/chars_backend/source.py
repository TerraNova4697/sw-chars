"""
Abstract method for SW data source.
"""

from abc import ABC, abstractmethod


class SWSource(ABC):

    @abstractmethod
    def get_chars(self, currency: str, to: str):
        pass
    