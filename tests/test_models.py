import dataclasses

import pytest

from tdd_based_api_service_stub.models import Forecast


def test_forecast_is_immutable() -> None:
    forecast = Forecast("London", 15.0, "Cloudy", 72, 18.0)

    with pytest.raises(dataclasses.FrozenInstanceError):
        forecast.temperature_celsius = 99.0  # type: ignore[misc]
