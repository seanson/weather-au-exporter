import os
import requests
import sys
import logging

from flask import Flask
from flask_apscheduler import APScheduler
from prometheus_client import Gauge
from prometheus_flask_exporter import PrometheusMetrics
from pyowm import OWM


class Config:
    SCHEDULER_API_ENABLED = True
    LOCATION = os.environ.get("LOCATION", "")
    OWM_API_KEY = os.environ.get("OWM_API_KEY", "")


if Config.LOCATION == "":
    print("LOCATION must be set!")
    sys.exit(1)

if Config.OWM_API_KEY == "":
    print("OWM_API_KEY must be set!")
    sys.exit(1)

owm = OWM(Config.OWM_API_KEY)
weather_manager = owm.weather_manager()

logger = logging.getLogger(__name__)
app = Flask(__name__)
app.config.from_object(Config())

metrics = PrometheusMetrics(app)
temp_gauge = Gauge(
    "weather_temperature_celcius",
    "The external temperature reported by the BOM API",
    labelnames=["location"],
)
humidity_gauge = Gauge(
    "weather_humidity_percentage",
    "The external humidity reported by the BOM API",
    labelnames=["location"],
)


scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@scheduler.task("interval", id="fetch_weather", minutes=30, misfire_grace_time=900)
def fetch_weather():
    logger.info("Fetching weather data for location %s", Config.LOCATION)
    weather_manager
    observation = weather_manager.weather_at_place(Config.LOCATION)
    temperature = observation.weather.temperature("celsius")["temp"]
    humidity = observation.weather.humidity
    temp_gauge.labels(location=Config.LOCATION).set(temperature)
    humidity_gauge.labels(location=Config.LOCATION).set(humidity)


fetch_weather()
