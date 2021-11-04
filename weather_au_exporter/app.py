import os
import requests
import sys
import logging

from flask import Flask
from flask_apscheduler import APScheduler
from datetime import datetime, timezone
from dateutil.parser import isoparse
from prometheus_client import Gauge
from prometheus_flask_exporter import PrometheusMetrics

class Config:
    SCHEDULER_API_ENABLED = True
    LOCATION_ID = os.environ.get("LOCATION_ID", "")

if Config.LOCATION_ID == "":
    print("LOCATION_ID must be set!")
    sys.exit(1)

weather_data = None
logger = logging.getLogger(__name__)
app = Flask(__name__)
app.config.from_object(Config())

metrics = PrometheusMetrics(app)
temp_gauge = Gauge("weather_temperature_celcius", "The external temperature reported by the BOM API", labelnames=["location"])

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@scheduler.task('interval', id='fetch_weather', minutes=30, misfire_grace_time=900)
def fetch_weather():
    global weather_data
    logger.info("Fetching weather data for location %s", Config.LOCATION_ID)
    url = f"https://api.weather.bom.gov.au/v1/locations/{Config.LOCATION_ID}/forecasts/hourly"
    response = requests.get("https://api.weather.bom.gov.au/v1/locations/r1r143/forecasts/hourly")
    weather_data = response.json()["data"]

@scheduler.task('interval', id='update_metrics', minutes=5, misfire_grace_time=900)
def weather_metrics():
    if weather_data is None:
        logger.warning("Weather data not ready yet")
        return
    logger.info("Updating weather metics")
    now = datetime.now(timezone.utc)
    closest = min(weather_data, key=lambda d: abs(isoparse(d["time"]) - now))
    temp_gauge.labels(location=Config.LOCATION_ID).set(closest["temp"])
    

fetch_weather()
weather_metrics()