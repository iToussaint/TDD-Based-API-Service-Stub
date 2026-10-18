"""The weather service: the public entry point for forecasts."""

import logging

from tdd_based_api_service_stub.exceptions import WeatherServiceError
from tdd_based_api_service_stub.models import Forecast, ForecastRequest
from tdd_based_api_service_stub.providers.base import WeatherProvider

logger = logging.getLogger(__name__)


class WeatherService:
    """Validate forecast requests, log them and delegate to a provider."""

    def __init__(self, provider: WeatherProvider) -> None:
        """Create the service.

        Args:
            provider: The source of forecast data.
        """
        self._provider = provider

    def get_forecast(self, city: str) -> Forecast:
        """Return the forecast for a city.

        Args:
            city: The city name. Case and extra whitespace are ignored.

        Returns:
            The forecast for the city.

        Raises:
            InvalidRequestError: If ``city`` is not a non-empty string.
            InvalidAPIKeyError: If the provider rejects the API key.
            CityNotFoundError: If the provider has no data for the city.
        """
        logger.info("forecast.request", extra={"city": city})
        try:
            request = ForecastRequest(city=city)
            forecast = self._provider.fetch_forecast(request)
        except WeatherServiceError as exc:
            logger.warning(
                "forecast.error",
                extra={"city": city, "error_type": type(exc).__name__},
            )
            raise
        logger.info(
            "forecast.response",
            extra={
                "city": forecast.city,
                "temperature_celsius": forecast.temperature_celsius,
                "condition": forecast.condition,
            },
        )
        return forecast
