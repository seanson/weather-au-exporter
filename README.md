# weather-au-exporter

This is a small exporter that pulls data from the Australian Bureau of Meteorology's website to provide local temperature information as a Prometheus metric.

This is currently used as part of a [Home Automation System](https://github.com/seanson/2018-pyconau-homekit-python) in order to provide outside temperature information compared to internal house temperature.

It is installable as a Helm chart -- see the [README](./helm/weather-au-exporter) for installation instructions.


## Configuration

This takes a single environment variable `LOCATION_ID` which can be found under the appropriate State / City designation on the [BOM Data Feeds](http://www.bom.gov.au/catalogue/data-feeds.shtml) site.