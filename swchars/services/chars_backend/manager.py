"""
Management class for characters operations.
"""
import json
import swchars

from swchars.services.chars_backend.api import SWAPI
from swchars.services.chars_backend.cache import SWCache
from swchars.exceptions.http_exceptions import ResponseBadRequest


class SWDataManager:
    """
    Management class for rates. Determines where to fetch data from.
    """
    items_endpoints = ['planets', 'films', 'vehicles', 'species', 'starships']

    def __init__(self):
        """
        Initialization function.

        Args:
            kwargs (dict): possible keys - from, to, value.
        """
        self.api = SWAPI()
        self.cache = SWCache()

    def get_chars(self, **kwargs):
        """
        Fetches chars from cache if exists, from API otherwise.

        Returns:
            dict for characters.
        """
        value = self.cache.get_chars(kwargs['page'][0])
        if value and not kwargs.get('clear_cache'):
            value = json.loads(value)
            value['source'] = 'cache'
        else:
            value = self.api.get_chars(kwargs['page'][0])
            value['source'] = 'api'
            self.cache.save_chars(kwargs['page'][0], json.dumps(value))

        del value['count']
        if value['next']:
            value['next'] = value['next'][-1]
        if value['previous']:
            value['previous'] = value['previous'][-1]

        return value

    def get_item(self, **kwargs) -> dict:
        """Fetch item from cache if exists, from API otherwise.

        Args:
            type (str): String representation of item type.
            id (int): Items ID.

        Returns:
            dict: Dict representation of items info.
        """
        if kwargs['type'][0] not in self.items_endpoints:
            raise ResponseBadRequest
        value = self.cache.get_item(kwargs['type'][0], kwargs['id'][0])
        if value and not kwargs.get('clear_cache'):
            value = json.loads(value)
            value['source'] = 'cache'
        else:
            value = self.api.get_item(kwargs['type'][0], kwargs['id'][0])
            value['source'] = 'api'
            self.cache.save_item(kwargs['type'][0], kwargs['id'][0], json.dumps(value))

        return value
