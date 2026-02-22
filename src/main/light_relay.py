"""
Author: Jake Brown
ID: 001239595
Purpose: class definition for light relay.
"""

import board
import gpiozero
import time


class LightRelay:
    def __init__(self):
        self.pin = 9
        self.state = False
        self.relay = gpiozero.OutputDevice(self.pin, active_high=False, initial_value=False)
        self.relay.off()
        
    def set_state(self, new_state):
        self.state = new_state

        if self.state:
            self.relay.on()

        else:
            self.relay.off()


def main():
    light = LightRelay()

    light.set_state(True)
    time.sleep(3)
    light.set_state(False)


if __name__ == "__main__":
    main()
