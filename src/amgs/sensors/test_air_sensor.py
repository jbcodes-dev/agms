"""
Author: Jake Brown
ID: 001239595
Purpose: uint tests for air sensor module.
"""

import unittest
from air_sensor import AirSensor


class AirSensorTests(unittest.TestCase):
    # based on adafruit_dht -> DHTBase.measure()
    # if failure to measure it raises RuntimeError
    # also can raise RuntimeError for checksum failure

    def test_sensor_wiring_correct(self):
        """ Raise Runtime Error if wiring is not correct. """
        air_sensor = AirSensor()

    def test_fetch_gets_data(self):
        """ Raise RuntimeError if fetch fails. """
        air_sensor = AirSensor()
        air_sensor.fetch()


def main():
    unittest.main()


if __name__ == "__main__":
    main()
