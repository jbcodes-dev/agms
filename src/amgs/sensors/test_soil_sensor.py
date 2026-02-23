"""
Author: Jake Brown
ID: 001239595
Purpose: unit tests for soil sensor module.
"""

import unittest
from soil_sensor import SoilSensor


class SoilSensorTests(unittest.TestCase):
    def test_wiring_correct(self):
        """ Raise RuntimeError if wiring is incorrect. """
        ss = SoilSensor()

    def test_fetch_gets_data(self):
        """ Raise RuntimeError if fetch fails. """
        ss = SoilSensor()
        ss.fetch()


def main():
    unittest.main()


if __name__ == "__main__":
    main()
    
