import pytest

from tdd_based_api_service_stub.models import Forecast, ForecastRequest
from tdd_based_api_service_stub.providers.base import WeatherProvider


def test_weather_provider_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        WeatherProvider()  # type: ignore[abstract]


def test_subclass_without_fetch_forecast_cannot_be_instantiated() -> None:
    class IncompleteProvider(WeatherProvider):
        pass

    with pytest.raises(TypeError):
        IncompleteProvider()  # type: ignore[abstract]


def test_subclass_with_fetch_forecast_can_be_instantiated() -> None:
    class CompleteProvider(WeatherProvider):
        def fetch_forecast(self, request: ForecastRequest) -> Forecast:
            return Forecast(request.city, 0.0, "Clear", 50, 0.0)

    assert isinstance(CompleteProvider(), WeatherProvider)
