"""Shared pytest fixtures."""

import pytest

from tdd_based_api_service_stub.service import WeatherService


@pytest.fixture
def weather_service() -> WeatherService:
    return WeatherService()
