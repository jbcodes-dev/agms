from skeleton import BaseSystem
from datetime import datetime

import time
import board
import adafruit_dht
from adafruit_seesaw.seesaw import seesaw

import RPi.GPIO as GPIO

class Terrarium(BaseSystem):

    class HumidityRegulation(BaseSystem.Subsystem):

        class HumiditySensor(BaseSystem.Subsystem.Module):
            def __init__(self, pin):
                super().__init__("DHT22", "Humidity Sensor")

                self._pin = pin         # type board.PIN
                self._temperature = 0   # type float
                self._humidity = 0      # type float

                self._dht = None

                self._setup()

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

            def _setup(self):
                """ Setup dht sensor using adafruit library """
                self._dht = adafruit.DHT22(self._pin)

            def fetch(self):
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

    class IrrigationSystem(BaseSystem.Subsystem):
        
        class SoilMoistureSensor(BaseSystem.Subsystem.Module):
            def __init__(self, pin):
                super().__init__("Capacitive Moisture Spade", "Soil Moisture Sensor")

                self._pin = pin
                
                self._soil_moisture = 0
                self._soil_temperature = 0
                
                self._i2c_bus = None 
                self._sensor = None

                self._setup()
            ### PROPERTIES ###

            @property
            def pin(self):
                return self._pin

            @property
            def soil_moisture(self):
                return self._soil_moisture

            @property
            def soil_temperature(self):
                return self._soil_temperature

            
            ### FUNCTIONALITY ###

            def _setup(self):
                """ setup sensor """
                self._bus = board.I2C()
                self._sensor = Seesaw(self._bus, add=0x36)


            def fetch(self):
                """ fetch soil moisture and temperature """
                print(f"LOG: fetching {self._name} readings for time {datatime.now()}")

                
                try:
                    self.soil_moisture = self._sensor.moisture_read()
                    self.soil_temperatre = self._sensor.temperature_read()

                    print(f"[{datetime.now()}] - T: {:.1f} | H: {.2f}")

                except RuntimeError as err:
                    self._sensor.exit()
                    print(err.args[0])
