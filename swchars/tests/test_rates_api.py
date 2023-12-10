"""
Test for the rates API.
"""
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from swchars.services.chars_backend.cache import SWCache


CHARS_URL = reverse('swchars:chars')
ITEMS_URL = reverse('swchars:items')


class CharsAPITests(TestCase):
    """Test cases for chars API.

    Args:
        TestCase (_type_): _description_
    """

    def setUp(self):
        self.client = APIClient()
        self.redis = SWCache()

    def test_chars_api_retrieve_chars_first_page(self):
        """Retrieve chars from API.
        """
        self.redis.flush_db()
        res = self.client.get(CHARS_URL, data={'page': '1'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['next'], '2')

    def test_chars_api_returns_10_chars(self):
        """Test Request returns 10 characters."""
        self.redis.flush_db()
        res = self.client.get(CHARS_URL, data={'page': '1'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data['results']) == 10)

    def test_chars_api_saves_cache(self):
        """Test Request returns returns cache."""
        self.redis.flush_db()
        res = self.client.get(CHARS_URL, data={'page': '1'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data['source'] == 'api')

        res = self.client.get(CHARS_URL, data={'page': '1'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data['source'] == 'cache')

    def test_chars_api_loads_correct_page(self):
        """Test chars endpoint sends correct page.
        """
        self.redis.flush_db()
        res = self.client.get(CHARS_URL, data={'page': '3'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['previous'], '2')
        self.assertEqual(res.data['next'], '4')

        res = self.client.get(CHARS_URL, data={'page': '5'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['previous'], '4')
        self.assertEqual(res.data['next'], '6')

    def test_chars_api_fetch_data_from_api_if_no_cache(self):
        """Test data fetched from API if no_cache is passed.
        """
        self.redis.flush_db()
        res = self.client.get(CHARS_URL, data={'page': '5'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['source'], 'api')

        res = self.client.get(CHARS_URL, data={'page': '5', 'no_cache': True})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['source'], 'api')

class ItemsAPITests(TestCase):
    """Test Cases for items API.

    Args:
        TestCase (_type_): _description_
    """

    def setUp(self):
        self.client = APIClient()
        self.redis = SWCache()

    def test_items_api_retrieve_single_item(self):
        """Test API returns single item.
        """
        self.redis.flush_db()
        res = self.client.get(ITEMS_URL, data={'id': '1', 'type': 'planets'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_items_api_saves_cache(self):
        """Test every item retrievable."""
        self.redis.flush_db()

        res = self.client.get(ITEMS_URL, data={'type': 'planets', 'id': '1'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data['source'] == 'api')

        res = self.client.get(ITEMS_URL, data={'type': 'planets', 'id': '1'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data['source'] == 'cache')

    def test_items_api_fetch_data_from_api_if_no_cache(self):
        """Test data fetched from API if no_cache is passed.
        """
        self.redis.flush_db()
        res = self.client.get(ITEMS_URL, data={'type': 'planets', 'id': '1'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['source'], 'api')

        res = self.client.get(ITEMS_URL, data={'type': 'planets', 'id': '1', 'no_cache': True})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['source'], 'api')
