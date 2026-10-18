# TDD-Based API Service Stub

A mock **Weather API** service built with strict **Test-Driven Development**.
It never calls a real API: it returns consistent, predefined data for known cities and
raises specific errors for invalid input.

## Quick start

Requires Python 3.11+.

```bash
# with Poetry
poetry install
poetry run coverage run -m pytest
poetry run coverage report

# or with pip
python -m venv .venv
.venv\Scripts\activate          # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
coverage run -m pytest
coverage report
```

## Usage

```python
from tdd_based_api_service_stub.exceptions import CityNotFoundError
from tdd_based_api_service_stub.logging_config import configure_logging
from tdd_based_api_service_stub.providers.mock_provider import MockWeatherProvider
from tdd_based_api_service_stub.service import WeatherService

configure_logging()  # optional: JSON logs on stderr

service = WeatherService(provider=MockWeatherProvider(api_key="demo-key-123"))

print(service.get_forecast("  kigali "))
# Forecast(city='Kigali', temperature_celsius=24.0, condition='Sunny', humidity_percent=65, wind_speed_kph=8.0)

try:
    service.get_forecast("Atlantis")
except CityNotFoundError as error:
    print(error)  # City not found: 'Atlantis'.
```

Known cities: London, Paris, Tokyo, New York, Kigali, Accra. Demo API key: `demo-key-123`.
City names are case- and whitespace-insensitive.

## Architecture

```
            ┌──────────────────────┐
 caller ──▶ │    WeatherService    │  validates (ForecastRequest), logs, delegates
            └──────────┬───────────┘
                       │ depends on the abstraction only
            ┌──────────▼───────────┐
            │ WeatherProvider (ABC)│  fetch_forecast(request) -> Forecast
            └──────────▲───────────┘
                       │ implements
       ┌───────────────┴───────────────┐
┌──────┴──────────────┐      ┌─────────┴──────────────┐
│ MockWeatherProvider │      │ (future) real provider │
│  predefined data    │      │  HTTP calls            │
└─────────────────────┘      └────────────────────────┘
```

| Module | Responsibility |
|---|---|
| `service.py` | `WeatherService` — validates the request, logs it, delegates to the provider |
| `providers/base.py` | `WeatherProvider` — the abstract interface |
| `providers/mock_provider.py` | `MockWeatherProvider` — predefined data and API key check |
| `models.py` | `ForecastRequest` (validated, normalised) and `Forecast` — frozen, type-hinted dataclasses |
| `exceptions.py` | `WeatherServiceError` and its subclasses |
| `logging_config.py` | `JsonFormatter` and `configure_logging()` for structured logs |

**SOLID:** `WeatherService` receives its provider through the constructor (dependency injection) and
depends only on the abstract `WeatherProvider` (dependency inversion). To use a real weather API,
write a new `WeatherProvider` subclass and pass it in — `WeatherService` does not change (open/closed).

## Error handling

All errors inherit from `WeatherServiceError`, so a single `except` can catch them all.

| Exception | Raised when |
|---|---|
| `InvalidRequestError` | the city is not a string, or is blank |
| `InvalidAPIKeyError` | the provider rejects the API key (the message never contains the key) |
| `CityNotFoundError` | the provider has no data for the city (`.city` holds the name) |

## Structured logging

| Event | Level | Fields |
|---|---|---|
| `forecast.request` | INFO | `city` |
| `forecast.response` | INFO | `city`, `temperature_celsius`, `condition` |
| `forecast.error` | WARNING | `city`, `error_type` |

With `configure_logging()`, each record is written as one JSON line:

```json
{"timestamp": "2026-10-19T01:04:37+0200", "level": "INFO", "logger": "tdd_based_api_service_stub.service", "event": "forecast.response", "city": "Kigali", "temperature_celsius": 24.0, "condition": "Sunny"}
```

## The TDD process

Every piece of logic was preceded by a failing test, following **Red → Green → Refactor**.
Each step is its own commit, so the cycles can be read directly from the history:

| Step | Commit prefix | Meaning |
|---|---|---|
| Red | `test: [RED] …` | a failing test describing the next behaviour |
| Green | `feat: [GREEN] …` | the minimum code to make it pass |
| Refactor | `refactor: [REFACTOR] …` | design improvements with all tests still green |
| Guard | `test: …` | a test that passes immediately and documents existing behaviour |

```bash
git log --oneline --reverse
```

Example cycles:

1. **First feature** — `test: [RED] get_forecast returns a forecast for a known city` →
   `feat: [GREEN] return a hardcoded forecast for London`; the next RED test (every known city)
   forced the hardcoded value into a lookup table.
2. **Validation moved into a model** — `test: [RED] ForecastRequest validates and normalises the city` →
   `feat: [GREEN] add a validated ForecastRequest dataclass` →
   `refactor: [REFACTOR] validate input through ForecastRequest in the service`.
3. **Dependency injection** — `test: [RED] WeatherService delegates to an injected WeatherProvider` →
   `feat: [GREEN] inject a WeatherProvider into WeatherService` →
   `refactor: [REFACTOR] isolate service tests with a mocked provider`.

Testing techniques used:

- **Fixtures** in `tests/conftest.py` set up the service client, a sample forecast and providers.
- **Parametrization** covers every known city and every invalid input with one test function each.
- **pytest-mock** — `mocker.create_autospec(WeatherProvider)` replaces the provider so service tests
  run in isolation; `side_effect` simulates provider errors.
- **caplog** asserts on the structured log records.

## Code quality

| Tool | Command |
|---|---|
| pytest + coverage.py (100% required, branch coverage) | `poetry run coverage run -m pytest` then `poetry run coverage report` |
| mypy (strict, src and tests) | `poetry run mypy` |
| black | `poetry run black .` |
| ruff (including Google-style docstring rules) | `poetry run ruff check .` |

black, ruff and mypy (on `src/`) run automatically through **pre-commit** hooks
(`poetry run pre-commit install`). pytest is deliberately not a hook, because RED commits contain
failing tests by design.

The latest coverage report is in [`docs/coverage-report.txt`](docs/coverage-report.txt).

## Git workflow

Trunk-based development: short-lived branches from `main`, merged only through pull requests
with a review, using merge commits so the TDD history stays visible. A merge conflict in
`README.md` between the architecture refactor and a docs branch was resolved in the refactor PR.
