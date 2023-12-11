"""
Custom exceptions for HTTP requests.
"""
from rest_framework.exceptions import APIException


class ResponseBadRequest(APIException):
    """
    Bad request exception.
    """
    status_code = 400
    default_detail = 'Unsupported item type.'
    default_code = 'service_unavailable'
    