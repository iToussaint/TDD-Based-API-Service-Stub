"""Shared pytest fixtures."""

import pytest

from tdd_based_api_service_stub.service import DEMO_API_KEY, WeatherService


@pytest.fixture
def weather_service() -> WeatherService:
    return WeatherService(api_key=DEMO_API_KEY)
