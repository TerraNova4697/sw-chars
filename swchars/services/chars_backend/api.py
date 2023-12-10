"""
Backend for getting characters from the external API.
"""
import requests
from rest_framework.exceptions import NotFound
from requests.exceptions import HTTPError, Timeout
import logging


from swchars.services.chars_backend.source import SWSource
from swchars.services.singleton import Singleton

BASE_URL = 'https://swapi.dev/api/'
logger = logging.getLogger('swchars')


class SWAPI(Singleton, SWSource):
    """Fetching characters from API."""

    def _base_request(self, **kwargs):
        """
        Base method for API request. Builds final response url and requests.

        Returns:
            str of response.
        """
        req_type = kwargs.get('req_type')

        if req_type == 'get':
            request_url = BASE_URL + kwargs.get('endpoint')
            headers = {"accept": "application/json"}

            params = kwargs.get('params')
            if params:
                request_url = request_url + params

            try:
                response = requests.get(url=request_url, headers=headers).json()
                if response.get('detail') == 'Not found':
                    raise NotFound
                return response
            except (HTTPError, Timeout) as e:
                logger.error(e)

    def get_chars(self, page: str = 1):
        """
        Fetching chars from external API.

        Returns:
            str of response
        """
        endpoint = f'people/?page={page}'
        return self._base_request(req_type='get', endpoint=endpoint)

    def _get_api_key(self):
        """Return api key needed for API request."""
        pass

    def get_item(self, item: str, id: int) -> dict:
        """Fetch item from API by its ID.

        Args:
            item (str): Item of corresponding endpoint
            id (int): Items ID.

        Returns:
            dict: Dict type representing item info.
        """
        endpoint = f'{item}/{id}'
        return self._base_request(req_type='get', endpoint=endpoint)

