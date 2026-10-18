import pytest

from tdd_based_api_service_stub.models import Forecast
from tdd_based_api_service_stub.service import WeatherService


def test_get_forecast_returns_forecast_for_known_city(
    weather_service: WeatherService,
) -> None:
    forecast = weather_service.get_forecast("London")

    assert isinstance(forecast, Forecast)
    assert forecast.city == "London"


@pytest.mark.parametrize(
    "expected",
    [
        Forecast("London", 15.0, "Cloudy", 72, 18.0),
        Forecast("Paris", 18.0, "Sunny", 55, 10.0),
        Forecast("Tokyo", 22.0, "Rainy", 80, 12.0),
        Forecast("New York", 20.0, "Partly Cloudy", 60, 15.0),
        Forecast("Kigali", 24.0, "Sunny", 65, 8.0),
        Forecast("Accra", 30.0, "Humid", 85, 14.0),
    ],
    ids=lambda forecast: forecast.city,
)
def test_get_forecast_returns_predefined_data_for_known_cities(
    weather_service: WeatherService, expected: Forecast
) -> None:
    assert weather_service.get_forecast(expected.city) == expected
