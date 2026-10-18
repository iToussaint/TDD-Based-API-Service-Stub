import logging

import pytest

from tdd_based_api_service_stub.exceptions import (
    CityNotFoundError,
    InvalidAPIKeyError,
    InvalidRequestError,
)
from tdd_based_api_service_stub.models import Forecast
from tdd_based_api_service_stub.service import WeatherService

SERVICE_LOGGER = "tdd_based_api_service_stub.service"


def _find_record(caplog: pytest.LogCaptureFixture, event: str) -> logging.LogRecord:
    return next(r for r in caplog.records if r.getMessage() == event)


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


@pytest.mark.parametrize(
    ("raw_city", "expected_city"),
    [
        ("london", "London"),
        ("  LONDON  ", "London"),
        ("new   york", "New York"),
    ],
)
def test_get_forecast_ignores_case_and_extra_whitespace(
    weather_service: WeatherService, raw_city: str, expected_city: str
) -> None:
    assert weather_service.get_forecast(raw_city).city == expected_city


def test_get_forecast_raises_city_not_found_for_unknown_city(
    weather_service: WeatherService,
) -> None:
    with pytest.raises(CityNotFoundError, match="Atlantis"):
        weather_service.get_forecast("Atlantis")


@pytest.mark.parametrize("city", ["", "   ", None, 123])
def test_get_forecast_rejects_invalid_city(
    weather_service: WeatherService, city: object
) -> None:
    with pytest.raises(InvalidRequestError):
        weather_service.get_forecast(city)  # type: ignore[arg-type]


@pytest.mark.parametrize("api_key", ["", "wrong-key"])
def test_get_forecast_rejects_invalid_api_key(api_key: str) -> None:
    service = WeatherService(api_key=api_key)

    with pytest.raises(InvalidAPIKeyError):
        service.get_forecast("London")


def test_get_forecast_logs_request(
    weather_service: WeatherService, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.INFO, logger=SERVICE_LOGGER)

    weather_service.get_forecast("London")

    record = _find_record(caplog, "forecast.request")
    assert record.levelno == logging.INFO
    assert vars(record)["city"] == "London"
