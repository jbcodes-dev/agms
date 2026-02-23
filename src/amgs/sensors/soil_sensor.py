"""
Author: Jake Brown
ID: 001239595
Purpose: class definition for soil sensor and its behaviour. 
"""

import time
import board
from adafruit_seesaw.seesaw import Seesaw


class SoilSensor:
    def __init__(self):
        """ Initialise Soil Sensor with correct pin and create sensor instance. """
        self.bus = board.I2C()
        self.temp = 0
        self.moisture = 0
        self.sensor = Seesaw(self.bus, addr=0x36)

    def fetch(self):
        """ Fetch soil moisture and temperature readings. """
        self.moisture = self.sensor.moisture_read()
        self.temp = self.sensor.get_temp()


def main():
    ss = SoilSensor()

    # test getting values every 10 seconds 5 times
    i = 0
    while i < 5:
        ss.fetch()
        print(f"[TEST] (Soil) M: {ss.moisture} | T: {ss.temp}")
        time.sleep(10)
        i += 1


if __name__ == "__main__":
    main()
