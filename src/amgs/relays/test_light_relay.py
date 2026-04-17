"""
Author: Jake Brown
ID: 001239595
Purpose: Unit test for Light Relay module.
"""

import unittest
from light_relay import LightRelay


class LightRelayTest(unittest.TestCase):
    def test_light_runs(self):
        """ Check visually if light works. """

        light = LightRelay()
        light.set_state(True)
        time.sleep(3)
        light.set_state(False)


def main():
    unittest.main()


if __name__ == "__main__":
    main()



