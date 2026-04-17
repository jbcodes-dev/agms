"""
Author: Jake Brown
ID: 001239595
Purpose: Unit test for Fan Relay module.
"""

import unittest
from fan_relay import FanRelay


class FanRelayTests(unittest.TestCase):
    def test_fan_runs(self):
        """ Check visually if fans working. """
        fanset1 = FanRelay(1)
        fanset2 = FanRelay(2)

        fanset1.set_state(True)
        time.sleep(3)
        fanset1.set_state(False)
        
        time.sleep(1)

        fanset2.set_state(True)
        time.sleep(3)
        fanset2.set_state(False)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
