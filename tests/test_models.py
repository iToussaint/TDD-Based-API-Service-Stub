import dataclasses

import pytest

from tdd_based_api_service_stub.exceptions import InvalidRequestError
from tdd_based_api_service_stub.models import Forecast, ForecastRequest


def test_forecast_is_immutable() -> None:
    forecast = Forecast("London", 15.0, "Cloudy", 72, 18.0)

    with pytest.raises(dataclasses.FrozenInstanceError):
        forecast.temperature_celsius = 99.0  # type: ignore[misc]


@pytest.mark.parametrize(
    ("raw_city", "expected"),
    [
        ("London", "London"),
        ("london", "London"),
        ("  LONDON  ", "London"),
        ("new   york", "New York"),
    ],
)
def test_forecast_request_normalises_city(raw_city: str, expected: str) -> None:
    assert ForecastRequest(city=raw_city).city == expected


@pytest.mark.parametrize("city", ["", "   ", None, 123])
def test_forecast_request_rejects_invalid_city(city: object) -> None:
    with pytest.raises(InvalidRequestError):
        ForecastRequest(city=city)  # type: ignore[arg-type]


def test_forecast_request_is_immutable() -> None:
    request = ForecastRequest(city="London")

    with pytest.raises(dataclasses.FrozenInstanceError):
        request.city = "Paris"  # type: ignore[misc]
