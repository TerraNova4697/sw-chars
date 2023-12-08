"""
Backend for getting characters from the external API.
"""
import requests
from requests.exceptions import HTTPError, Timeout
import logging


from swchars.services.chars_backend.source import SWSource
from swchars.services.singleton import Singleton

BASE_URL = ''
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
            headers = {"accept": "text/plain"}

            params = kwargs.get('params')
            if params:
                request_url = request_url + params

            try:
                response = requests.get(url=request_url, headers=headers)
                return response.text
            except (HTTPError, Timeout) as e:
                logger.error(e)

    def get_chars(self, currency: str, to: str):
        """
        Fetching chars from external API.

        Returns:
            str of response
        """
        endpoint = f''
        return self._base_request(req_type='get', endpoint=endpoint)

    def _get_api_key(self):
        """Return api key needed for API request."""
        pass