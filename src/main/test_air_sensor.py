import unittest

from air_sensor import AirSensor


class AirSensorTests(unittest.TestCase):
    def test_fetch_gets_data(self):
        with self.assertRaises(RuntimeError):
            air_sensor = AirSensor()
            air_sensor.fetch()
