import pytest

from tdd_based_api_service_stub.exceptions import (
    CityNotFoundError,
    InvalidAPIKeyError,
    InvalidRequestError,
    WeatherServiceError,
)


@pytest.mark.parametrize(
    "error_class",
    [
        CityNotFoundError,
        InvalidAPIKeyError,
        InvalidRequestError,
    ],
)
def test_all_custom_errors_inherit_from_weather_service_error(
    error_class: type[Exception],
) -> None:
    assert issubclass(error_class, WeatherServiceError)


def test_city_not_found_error_keeps_city_and_mentions_it() -> None:
    error = CityNotFoundError("Atlantis")

    assert error.city == "Atlantis"
    assert "Atlantis" in str(error)


def test_invalid_api_key_error_has_a_helpful_message() -> None:
    assert str(InvalidAPIKeyError()) == "The provided API key is invalid."
