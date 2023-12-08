"""
Redis cache class for caching rates.
"""
import redis
import logging

from django.conf import settings

logger = logging.getLogger('swchars')

from swchars.services.chars_backend.source import SWSource
from swchars.services.singleton import Singleton


class SWCache(Singleton, SWSource):
    """Redis chache class."""

    def __init__(self):
        try:
            self._redis = redis.Redis(
                host=settings.SW_CACHE['host'],
                password=settings.SW_CACHE['password']
            )
        except Exception as e:
            logger.error(e)

    def get_chars(self, key: str):
        """
        Returns string representation of chars if exists in cache and still valid. Otherwise returns None.

        Returns:
            str of rates OR None if does not exist.
        """
        try:
            return self._redis.get(key)
        except Exception as e:
            logger.error(e)

    def save_chars(self, key: str, value: str):
        """
        Saves given currencies as a key and its rates as value for one hour.
        """
        hour_in_sec = 60*60*60
        self._redis.set(name=key, value=value, ex=hour_in_sec)

    def flush_db(self):
        """
        Flush all data in Redis.
        """
        self._redis.flushdb()