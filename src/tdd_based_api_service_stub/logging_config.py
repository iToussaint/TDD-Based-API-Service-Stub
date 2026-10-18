"""Structured (JSON) logging for the weather service."""

import json
import logging
from typing import Final

PACKAGE_LOGGER_NAME: Final = "tdd_based_api_service_stub"

_STANDARD_RECORD_ATTRS: Final = frozenset(vars(logging.makeLogRecord({}))) | {
    "message",
    "asctime",
}


class JsonFormatter(logging.Formatter):
    """Format log records as single-line JSON objects.

    Any fields passed through ``extra=`` are added to the JSON object, which
    makes the logs easy to search and parse.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Convert a log record into a JSON string.

        Args:
            record: The log record to format.

        Returns:
            The record as a JSON string.
        """
        payload: dict[str, object] = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "event": record.getMessage(),
        }
        payload.update(
            (key, value)
            for key, value in vars(record).items()
            if key not in _STANDARD_RECORD_ATTRS
        )
        return json.dumps(payload, default=str)


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    """Send the package's logs to stderr as JSON.

    Calling this function more than once does not add duplicate handlers.

    Args:
        level: The minimum level to log.

    Returns:
        The configured package logger.
    """
    logger = logging.getLogger(PACKAGE_LOGGER_NAME)
    logger.setLevel(level)
    if not any(isinstance(h.formatter, JsonFormatter) for h in logger.handlers):
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
    return logger
