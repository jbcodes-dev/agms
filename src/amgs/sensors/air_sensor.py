"""
Author: Jake Brown
ID: 001239595
Purpose: Class Definition for Air Sensor and test its behaviour.
"""

import time
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


def main():
    dht = AirSensor()

    # test getting values every 10 seconds 5 times
    i = 0
    
    while i < 5:
        dht.fetch()
        print(f"[TEST] (Air) T: {dht.temp} | H: {dht.humidity}")
        time.sleep(10)
        i += 1
    
    dht.cleanup()


if __name__ == "__main__":
    main()
