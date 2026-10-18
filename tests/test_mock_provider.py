import pytest

from tdd_based_api_service_stub.exceptions import CityNotFoundError, InvalidAPIKeyError
from tdd_based_api_service_stub.models import Forecast, ForecastRequest
from tdd_based_api_service_stub.providers.base import WeatherProvider
from tdd_based_api_service_stub.providers.mock_provider import MockWeatherProvider


def test_mock_provider_is_a_weather_provider(
    mock_weather_provider: MockWeatherProvider,
) -> None:
    assert isinstance(mock_weather_provider, WeatherProvider)


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
def test_fetch_forecast_returns_predefined_data_for_known_cities(
    mock_weather_provider: MockWeatherProvider, expected: Forecast
) -> None:
    request = ForecastRequest(city=expected.city)

    assert mock_weather_provider.fetch_forecast(request) == expected


def test_fetch_forecast_raises_city_not_found_for_unknown_city(
    mock_weather_provider: MockWeatherProvider,
) -> None:
    with pytest.raises(CityNotFoundError) as exc_info:
        mock_weather_provider.fetch_forecast(ForecastRequest(city="Atlantis"))

    assert exc_info.value.city == "Atlantis"


@pytest.mark.parametrize("api_key", ["", "wrong-key"])
def test_fetch_forecast_rejects_invalid_api_key(api_key: str) -> None:
    provider = MockWeatherProvider(api_key=api_key)

    with pytest.raises(InvalidAPIKeyError):
        provider.fetch_forecast(ForecastRequest(city="London"))
