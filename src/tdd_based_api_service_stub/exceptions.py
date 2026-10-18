"""Custom exceptions raised by the weather service."""


class CityNotFoundError(Exception):
    """Raised when no forecast exists for the requested city."""


class InvalidRequestError(Exception):
    """Raised when the request parameters are invalid (e.g. an empty city)."""


class InvalidAPIKeyError(Exception):
    """Raised when the API key is missing or not recognised."""
