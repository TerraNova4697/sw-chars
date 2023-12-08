"""
Management class for characters operations.
"""
from converter.services.rates_backend.rates_api import RatesAPI
from converter.services.rates_backend.rates_cache import RatesCache


class RatesManager:
    """
    Management class for rates. Determines where to fetch data from.
    """

    def __init__(self, **kwargs):
        """
        Initialization function.

        Args:
            kwargs (dict): possible keys - from, to, value.
        """
        pass

    def get_rates(self):
        """
        Fetches rates.

        Returns:
            dict for characters.
        """
        pass