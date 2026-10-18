"""The weather service: the public entry point for forecasts."""

from tdd_based_api_service_stub.models import Forecast


class WeatherService:
    """Provide weather forecasts for a predefined set of cities."""

    def get_forecast(self, city: str) -> Forecast:
        """Return the forecast for a city.

        Args:
            city: The city name.

        Returns:
            The forecast for the city.
        """
        return Forecast("London", 15.0, "Cloudy", 72, 18.0)
