from tdd_based_api_service_stub.models import Forecast
from tdd_based_api_service_stub.service import WeatherService


def test_get_forecast_returns_forecast_for_known_city() -> None:
    service = WeatherService()

    forecast = service.get_forecast("London")

    assert isinstance(forecast, Forecast)
    assert forecast.city == "London"
