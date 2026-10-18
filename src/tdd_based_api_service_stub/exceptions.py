"""Custom exceptions raised by the weather service."""


class WeatherServiceError(Exception):
    """Base class for every error raised by the weather service."""


class InvalidRequestError(WeatherServiceError):
    """Raised when the request parameters are invalid (e.g. an empty city)."""


class InvalidAPIKeyError(WeatherServiceError):
    """Raised when the API key is missing or not recognised."""

    def __init__(self) -> None:
        """Create the error with a fixed message that never contains the key."""
        super().__init__("The provided API key is invalid.")


class CityNotFoundError(WeatherServiceError):
    """Raised when no forecast exists for the requested city.

    Attributes:
        city: The city that could not be found.
    """

    def __init__(self, city: str) -> None:
        """Create the error for a specific city.

        Args:
            city: The city that could not be found.
        """
        self.city = city
        super().__init__(f"City not found: {city!r}.")
