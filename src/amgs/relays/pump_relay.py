"""
Author: Jake Brown
ID: 001239595
Purpose: class definition for water pump relay.
"""

import time
from datetime import datetime, timedelta
import gpiozero


class PumpRelay:
    def __init__(self):
        self.pin = 10
        self.state = False
        self.relay = gpiozero.OutputDevice(self.pin, active_high=False, initial_value=False)
        self.relay.off()
        self.interval = timedelta(hours=24)
        self.next_activation = datetime.now()

    def set_state(self, new_state):
        self.state = new_state
        
        if self.state:
            self.relay.on()

        else:
            self.relay.off()
            self.next_activation += self.interval


def main():
    pump = PumpRelay()

    pump.set_state(True)
    time.sleep(3)
    pump.set_state(False)


if __name__ == "__main__":
    main()
