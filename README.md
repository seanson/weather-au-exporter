# weather-au-exporter

This is a small exporter that pulls data from the [OpenWeatherMap API](https://openweathermap.org/) to provide local temperature information as a Prometheus metric.

This is currently used as part of a [Home Automation System](https://github.com/seanson/2018-pyconau-homekit-python) in order to provide outside temperature information compared to internal house temperature.

It is installable as a Helm chart -- see the [README](./helm/weather-au-exporter) for installation instructions.


## Configuration

This requires the following env vars:
- `LOCATION` - City name in the format required by the [API](https://openweathermap.org/current#name)
- `OWM_API_KEY` - An API key generated in the [OpenWeatherMap Console](https://home.openweathermap.org/api_keys)
