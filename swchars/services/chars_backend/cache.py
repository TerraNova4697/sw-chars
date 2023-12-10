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

    def __init__(self, host: str = None, password = None):
        if not host:
            host = settings.SW_CACHE['host']
        if not password:
            password = settings.SW_CACHE['password']
        try:
            self._redis = redis.Redis(
                host=host,
                password=password
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
            return self._redis.hget(f'chars:{key}', key)
        except Exception as e:
            logger.error(e)
            return None

    def save_chars(self, key: str, value: dict):
        """
        Saves given currencies as a key and its rates as value for one hour.
        """
        name, ex = f'chars:{key}', 60*10
        self._redis.hset(name=name, key=key, value=value)
        self._redis.expire(name, ex)

    def get_item(self, type: str, key: str) -> bytes|None:
        """Returns bytes representation of item if in cache. None otherwise.

        Args:
            type (str): Type of item.
            key (str): ID of item.

        Returns:
            bytes|None: _description_
        """
        try:
            return self._redis.hget(f'{type}:{key}', key)
        except Exception as e:
            logger.error(e)
            return None

    def save_item(self, type: str, key: str, value: dict):
        """Save given item in cache.

        Args:
            type (str): Type of item.
            key (str): ID of item.
            value (dict): Dict representation of item.
        """
        name, ex = f'{type}:{key}', 60*10
        self._redis.hset(name=name, key=key, value=value)
        self._redis.expire(name, ex)

    def flush_db(self):
        """
        Flush all data in Redis.
        """
        self._redis.flushdb()