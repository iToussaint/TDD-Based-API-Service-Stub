import json
import logging
from collections.abc import Iterator

import pytest

from tdd_based_api_service_stub.logging_config import (
    PACKAGE_LOGGER_NAME,
    JsonFormatter,
    configure_logging,
)


@pytest.fixture
def package_logger() -> Iterator[logging.Logger]:
    """Give a test the package logger and restore it afterwards."""
    logger = logging.getLogger(PACKAGE_LOGGER_NAME)
    original_handlers = logger.handlers[:]
    original_level = logger.level
    yield logger
    logger.handlers = original_handlers
    logger.setLevel(original_level)


def _make_record(**extra: object) -> logging.LogRecord:
    return logging.makeLogRecord(
        {
            "name": "tdd_based_api_service_stub.service",
            "levelno": logging.INFO,
            "levelname": "INFO",
            "msg": "forecast.request",
            **extra,
        }
    )


def test_json_formatter_outputs_standard_fields() -> None:
    output = json.loads(JsonFormatter().format(_make_record()))

    assert output["level"] == "INFO"
    assert output["logger"] == "tdd_based_api_service_stub.service"
    assert output["event"] == "forecast.request"
    assert "timestamp" in output


def test_json_formatter_includes_extra_fields() -> None:
    output = json.loads(JsonFormatter().format(_make_record(city="London")))

    assert output["city"] == "London"


def test_configure_logging_attaches_one_json_handler(
    package_logger: logging.Logger,
) -> None:
    configure_logging()

    json_handlers = [
        h for h in package_logger.handlers if isinstance(h.formatter, JsonFormatter)
    ]
    assert len(json_handlers) == 1


def test_configure_logging_twice_does_not_duplicate_handlers(
    package_logger: logging.Logger,
) -> None:
    configure_logging()
    configure_logging()

    json_handlers = [
        h for h in package_logger.handlers if isinstance(h.formatter, JsonFormatter)
    ]
    assert len(json_handlers) == 1


def test_configure_logging_sets_level(package_logger: logging.Logger) -> None:
    configure_logging(level=logging.DEBUG)

    assert package_logger.level == logging.DEBUG
