"""The weather service: the public entry point for forecasts."""

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from tdd_based_api_service_stub.exceptions import CityNotFoundError
from tdd_based_api_service_stub.models import Forecast, ForecastRequest

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


class WeatherService:
    """Provide weather forecasts for a predefined set of cities."""

    def get_forecast(self, city: str) -> Forecast:
        """Return the forecast for a city.

        Args:
            city: The city name. Case and extra whitespace are ignored.

        Returns:
            The forecast for the city.

        Raises:
            InvalidRequestError: If ``city`` is not a non-empty string.
            CityNotFoundError: If there is no data for the city.
        """
        request = ForecastRequest(city=city)
        try:
            return KNOWN_FORECASTS[request.city]
        except KeyError:
            raise CityNotFoundError(f"City not found: {request.city!r}.") from None
