"""
Author: Jake Brown
ID: 001239595
Purpose: class definition for Air Sensor.
"""

import board
import adafruit_dht


class AirSensor:
    def __init__(self):
        """ Initialise AirSensor with correct pin and create sensor instance. """

        self.pin = board.D4
        self.temp = 0
        self.humidity = 0
        self.sensor = adafruit_dht.DHT22(self.pin)

    def fetch(self):
        """ Fetch temperature and humidity from dht sensor. """

        # dht's can be tempermental, sometimes they won't read anything
        try:
            self.temp = self.sensor.temperature
            self.humidity = self.sensor.humidity

        # if it doesn't read, keep last results
        except RuntimeError as err:
            print(f"[ERROR] {err.args[0]}")


    def cleanup(self):
        """ Cleanup DHT sensor before program exit. """

        # log debug statement here
        self.sensor.exit()
