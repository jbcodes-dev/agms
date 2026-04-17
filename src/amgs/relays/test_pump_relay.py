"""
Author: Jake Brown
ID: 001239595
Purpose: Unit test for Pump Relay module.
"""

import unittest
from pump_relay import PumpRelay


class PumpRelayTest(unittest.TestCase):
    def test_fan_runs(self):
        """ Check visually if pump works. """
        pump = PumpRelay()

        pump.set_state(True)
        time.sleep(3)
        pump.set_state(False)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
