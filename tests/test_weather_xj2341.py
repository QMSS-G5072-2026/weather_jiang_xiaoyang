import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

import weather_xj2341
from weather_xj2341 import (
    celsius_to_fahrenheit,
    clean_readings,
    summarize_temperatures,
)


def test_version_is_defined():
    assert isinstance(weather_xj2341.__version__, str)


@pytest.mark.parametrize(
        "celsius, expected",
        [
            (0, 32),
            (100, 212),
            (-40, -40),
            (37, 98.6),
            (-273.15, -459.67),
        ],
)
def test_celsius_to_fahrenheit(celsius, expected):
    """Check Celsius-to-Fahrenheit conversion for representative temperatures."""
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected)

@pytest.mark.parametrize(
        "bad_input, expected_error",
        [
            ("37", TypeError),
            (None, TypeError),
            (True, TypeError),
            (-273.1501, ValueError),
        ],
)
def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    """Check that invalid inputs raise the documented exception."""
    with pytest.raises(expected_error):
        celsius_to_fahrenheit(bad_input)

def test_summarize_temperatures():
    """Check that summaries ignore NaN and return all four statistics."""
    # Arrange: prepare readings with one missing temperature
    temps = [10.0, float("nan"), 20.0]
    # Act: summarize the readings
    summary = summarize_temperatures(temps)

    # Assert: check the keys and their expected values
    assert set(summary) == {"mean", "min", "max", "n_missing"}
    assert summary["mean"] == pytest.approx(15.0)
    assert summary["min"] == pytest.approx(10.0)
    assert summary["max"] == pytest.approx(20.0)
    assert summary["n_missing"] == 1


@pytest.fixture
def raw_readings():
    """Provide unsorted raw readings with one missing and one implausible value."""
    return pd.DataFrame({
        "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
        "date": [
            "2026-07-02",
            "2026-07-01",
            "2026-07-01",
            "2026-07-02",
            "2026-07-01",
        ],
        "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
    })

def test_raw_readings_fixture(raw_readings):
    """Check the fixture's columns, row count, and missing temperature."""
    assert list(raw_readings.columns) == ["station", "date", "temp_c"]
    assert len(raw_readings) == 5
    assert raw_readings["temp_c"].isna().sum() == 1

def test_clean_readings(raw_readings):
    """Check that readings are cleaned, converted, sorted, and reindexed."""
    expected = pd.DataFrame({
        "station": ["CPK", "JFK", "LGA"],
        "date": ["2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [25.0, 30.0, 28.0],
        "temp_f": [77.0, 86.0, 82.4],
    })
    actual = clean_readings(raw_readings)
    assert_frame_equal(actual, expected)
