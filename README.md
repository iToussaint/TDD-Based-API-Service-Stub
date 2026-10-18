# TDD-Based API Service Stub

A mock Weather API service built with strict Test-Driven Development (TDD).

## Architecture

`WeatherService` depends on the abstract `WeatherProvider` interface.
`MockWeatherProvider` implements it with predefined data, so a real
HTTP-based provider can replace it without changing the service.
