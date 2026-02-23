"""
Author: Jake Brown
ID: 001239595
Purpose: class definition for fan relay.
"""

import board
import time
import gpiozero


class FanRelay:
    def __init__(self, group):
        if group == 1:
            self.pin = 23
        elif group == 2:
            self.pin = 24
        else:
            raise RuntimeError("[ERROR] invalid fan group selected, must be '1' or '2'.")

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
    fanset1 = FanRelay(1)
    fanset2 = FanRelay(2)

    fanset1.set_state(True)
    time.sleep(3)
    fanset1.set_state(False)
    
    time.sleep(1)

    fanset2.set_state(True)
    time.sleep(3)
    fanset2.set_state(False)


if __name__ == "__main__":
    main()
