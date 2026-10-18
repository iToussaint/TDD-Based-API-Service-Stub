"""A mock weather provider that returns predefined data."""

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from tdd_based_api_service_stub.exceptions import CityNotFoundError, InvalidAPIKeyError
from tdd_based_api_service_stub.models import Forecast, ForecastRequest
from tdd_based_api_service_stub.providers.base import WeatherProvider

DEMO_API_KEY: Final = "demo-key-123"
VALID_API_KEYS: Final = frozenset({DEMO_API_KEY})

KNOWN_FORECASTS: Final[Mapping[str, Forecast]] = MappingProxyType(
    {
        "London": Forecast("London", 15.0, "Cloudy", 72, 18.0),
        "Paris": Forecast("Paris", 18.0, "Sunny", 55, 10.0),
        "Tokyo": Forecast("Tokyo", 22.0, "Rainy", 80, 12.0),
        "New York": Forecast("New York", 20.0, "Partly Cloudy", 60, 15.0),
        "Kigali": Forecast("Kigali", 24.0, "Sunny", 65, 8.0),
        "Accra": Forecast("Accra", 30.0, "Humid", 85, 14.0),
    }
)


class MockWeatherProvider(WeatherProvider):
    """Simulate an external weather API with fixed, predictable data."""

    def __init__(self, api_key: str) -> None:
        """Create the provider.

        Args:
            api_key: The API key sent with every request.
        """
        self._api_key = api_key

    def fetch_forecast(self, request: ForecastRequest) -> Forecast:
        """Return the predefined forecast for the requested city.

        Args:
            request: A validated forecast request.

        Returns:
            The predefined forecast for ``request.city``.

        Raises:
            InvalidAPIKeyError: If the API key is not recognised.
            CityNotFoundError: If the city is not in the predefined data.
        """
        if self._api_key not in VALID_API_KEYS:
            raise InvalidAPIKeyError()
        try:
            return KNOWN_FORECASTS[request.city]
        except KeyError:
            raise CityNotFoundError(request.city) from None
