import logging
from unittest.mock import NonCallableMagicMock

import pytest

from tdd_based_api_service_stub.exceptions import (
    CityNotFoundError,
    InvalidAPIKeyError,
    InvalidRequestError,
    WeatherServiceError,
)
from tdd_based_api_service_stub.models import Forecast, ForecastRequest
from tdd_based_api_service_stub.providers.base import WeatherProvider
from tdd_based_api_service_stub.providers.mock_provider import MockWeatherProvider
from tdd_based_api_service_stub.service import WeatherService

SERVICE_LOGGER = "tdd_based_api_service_stub.service"


def _find_record(caplog: pytest.LogCaptureFixture, event: str) -> logging.LogRecord:
    return next(r for r in caplog.records if r.getMessage() == event)


# --- Delegation to the provider -------------------------------------------


def test_get_forecast_returns_forecast_from_provider(
    weather_service: WeatherService, sample_forecast: Forecast
) -> None:
    assert weather_service.get_forecast("London") == sample_forecast


def test_get_forecast_calls_provider_once_with_normalised_request(
    weather_service: WeatherService, mock_provider: NonCallableMagicMock
) -> None:
    weather_service.get_forecast("  london ")

    mock_provider.fetch_forecast.assert_called_once_with(ForecastRequest(city="London"))


# --- Error handling ---------------------------------------------------------


@pytest.mark.parametrize("city", ["", "   ", None, 123])
def test_get_forecast_rejects_invalid_city_without_calling_provider(
    weather_service: WeatherService,
    mock_provider: NonCallableMagicMock,
    city: object,
) -> None:
    with pytest.raises(InvalidRequestError):
        weather_service.get_forecast(city)  # type: ignore[arg-type]

    mock_provider.fetch_forecast.assert_not_called()


@pytest.mark.parametrize("error", [CityNotFoundError("Atlantis"), InvalidAPIKeyError()])
def test_get_forecast_propagates_provider_errors(
    weather_service: WeatherService,
    mock_provider: NonCallableMagicMock,
    error: WeatherServiceError,
) -> None:
    mock_provider.fetch_forecast.side_effect = error

    with pytest.raises(type(error)):
        weather_service.get_forecast("Atlantis")


# --- Structured logging ------------------------------------------------------


def test_get_forecast_logs_request(
    weather_service: WeatherService, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.INFO, logger=SERVICE_LOGGER)

    weather_service.get_forecast("London")

    record = _find_record(caplog, "forecast.request")
    assert record.levelno == logging.INFO
    assert vars(record)["city"] == "London"


def test_get_forecast_logs_response(
    weather_service: WeatherService, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.INFO, logger=SERVICE_LOGGER)

    weather_service.get_forecast("London")

    record = _find_record(caplog, "forecast.response")
    assert record.levelno == logging.INFO
    assert vars(record)["city"] == "London"
    assert vars(record)["temperature_celsius"] == 15.0
    assert vars(record)["condition"] == "Cloudy"


@pytest.mark.parametrize(
    ("error", "expected_type"),
    [
        (CityNotFoundError("Atlantis"), "CityNotFoundError"),
        (InvalidAPIKeyError(), "InvalidAPIKeyError"),
    ],
)
def test_get_forecast_logs_provider_errors_as_warnings(
    weather_service: WeatherService,
    mock_provider: NonCallableMagicMock,
    caplog: pytest.LogCaptureFixture,
    error: WeatherServiceError,
    expected_type: str,
) -> None:
    caplog.set_level(logging.INFO, logger=SERVICE_LOGGER)
    mock_provider.fetch_forecast.side_effect = error

    with pytest.raises(WeatherServiceError):
        weather_service.get_forecast("Atlantis")

    record = _find_record(caplog, "forecast.error")
    assert record.levelno == logging.WARNING
    assert vars(record)["error_type"] == expected_type


def test_get_forecast_logs_invalid_request_as_warning(
    weather_service: WeatherService, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.INFO, logger=SERVICE_LOGGER)

    with pytest.raises(InvalidRequestError):
        weather_service.get_forecast("   ")

    record = _find_record(caplog, "forecast.error")
    assert record.levelno == logging.WARNING
    assert vars(record)["error_type"] == "InvalidRequestError"


# --- Architecture (integration and swappability) -----------------------------


def test_service_works_end_to_end_with_mock_provider(
    mock_weather_provider: MockWeatherProvider,
) -> None:
    service = WeatherService(provider=mock_weather_provider)

    forecast = service.get_forecast("  new   york ")

    assert forecast == Forecast("New York", 20.0, "Partly Cloudy", 60, 15.0)


def test_service_accepts_any_weather_provider_implementation() -> None:
    class FakeProvider(WeatherProvider):
        def fetch_forecast(self, request: ForecastRequest) -> Forecast:
            return Forecast(request.city, -5.0, "Snowy", 90, 30.0)

    service = WeatherService(provider=FakeProvider())

    assert service.get_forecast("Oslo") == Forecast("Oslo", -5.0, "Snowy", 90, 30.0)
