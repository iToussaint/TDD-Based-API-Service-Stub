"""Shared pytest fixtures."""

import pytest

from tdd_based_api_service_stub.providers.mock_provider import MockWeatherProvider
from tdd_based_api_service_stub.service import DEMO_API_KEY, WeatherService


@pytest.fixture
def weather_service() -> WeatherService:
    return WeatherService(api_key=DEMO_API_KEY)


@pytest.fixture
def mock_weather_provider() -> MockWeatherProvider:
    return MockWeatherProvider(api_key=DEMO_API_KEY)
