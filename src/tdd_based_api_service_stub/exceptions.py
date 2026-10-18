"""Custom exceptions raised by the weather service."""


class CityNotFoundError(Exception):
    """Raised when no forecast exists for the requested city."""
