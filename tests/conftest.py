"""Shared pytest fixtures."""

from unittest.mock import NonCallableMagicMock

import pytest
from pytest_mock import MockerFixture

from tdd_based_api_service_stub.models import Forecast
from tdd_based_api_service_stub.providers.base import WeatherProvider
from tdd_based_api_service_stub.providers.mock_provider import (
    DEMO_API_KEY,
    MockWeatherProvider,
)
from tdd_based_api_service_stub.service import WeatherService


@pytest.fixture
def sample_forecast() -> Forecast:
    return Forecast("London", 15.0, "Cloudy", 72, 18.0)


@pytest.fixture
def mock_provider(
    mocker: MockerFixture, sample_forecast: Forecast
) -> NonCallableMagicMock:
    provider: NonCallableMagicMock = mocker.create_autospec(
        WeatherProvider, instance=True
    )
    provider.fetch_forecast.return_value = sample_forecast
    return provider


@pytest.fixture
def weather_service(mock_provider: NonCallableMagicMock) -> WeatherService:
    return WeatherService(provider=mock_provider)


@pytest.fixture
def mock_weather_provider() -> MockWeatherProvider:
    return MockWeatherProvider(api_key=DEMO_API_KEY)
