from skeleton import BaseSystem
from datetime import datetime

import time
import board
import adafruit_dht

import RPi.GPIO as GPIO

class Terrarium(BaseSystem):

    class HumidityRegulation(BaseSystem.Subsystem):

        class HumiditySensor(BaseSystem.Subsystem.Module):
            def __init__(self, pin):
                super().__init__("DHT22", "Humidity Sensor")

                self._pin = pin         # type board.PIN
                self._temperature = 0   # type float
                self._humidity = 0      # type float

                self._dht = adafruit_dht.DHT22(self._pin)

            ### PROPERTIES ###

            @property
            def pins(self):
                return self._pins

            @property
            def temperature(self):
                return self._temperature

            @temperature.setter
            def temperature(self, new_temperature):
                self._temperature = new_temperature

            @property
            def humidity(self):
                return self._humidity

            @humidity.setter
            def humidity(self, new_humidity):
                self._humidity = new_humidity

            ### FUNCTIONALITY ###

            def fetch_reading(self):
                print(f"LOG: fetching {self._name} readings for time {datatime.now()}")

                try:
                    self.temperature = self._dht.temperature
                    self.humidity = self._dht.humidity

                    print(f"[{datetime.now()}] - T: {:.1f} | H: {.2f}")

                except RuntimeError as err:
                    self._dht.exit()
                    print(err.args[0])


        class AirflowRelay(BaseSystem.Subsystem.Module):
            def __init__(self, pin):
                super().__init__("RPi Cooling Fans", "Airflow Relay")

                self._pin = pin
                self._relay_state = False

            ### PROPERTIES ###

            @property
            def pin(self):
                return self._pin

            @property
            def relay_state(self):
                return self._relay_state

            ### FUNCTIONALITY ###

            def change_relay_state(self, new_state)
                    print("LOG: changing fan state")

                    if new_state:
                        GPIO.output(self.pin, GPIO.HIGH)
                        self.relay_state = True

                    else:
                        GPIO.output(self.pin, GPIO.LOW)
                        self.relay_state = False
