"""The abstract interface every weather provider implements."""

from abc import ABC, abstractmethod

from tdd_based_api_service_stub.models import Forecast, ForecastRequest


class WeatherProvider(ABC):
    """A source of weather forecasts.

    ``WeatherService`` depends only on this interface, so the mock provider
    can be swapped for a real HTTP-based one without changing the service.
    """

    @abstractmethod
    def fetch_forecast(self, request: ForecastRequest) -> Forecast:
        """Fetch the forecast for the requested city.

        Args:
            request: A validated forecast request.

        Returns:
            The forecast for ``request.city``.
        """
