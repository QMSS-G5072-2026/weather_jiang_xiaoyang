# read version from installed package
from importlib.metadata import version
__version__ = version("weather_xj2341")

from .weather_xj2341 import (
    celsius_to_fahrenheit,
    summarize_temperatures,
    clean_readings,
)