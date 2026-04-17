"""
Author: Jake Brown
ID: 001239595
Purpose: class definition for main application module.
"""

import time
from datetime import datetime, timedelta
import gpiozero

from amgs.sensors.air_sensor import AirSensor
from amgs.sensors.soil_sensor import SoilSensor

from amgs.relays.light_relay import LightRelay
from amgs.relays.fan_relay import FanRelay
from amgs.relays.pump_relay import PumpRelay

from amgs.misc.rpi_camera import RPiCamera
from amgs.misc.dbhandler import DBHandler

from amgs.algorithm.airflow_algorithm import AirflowAlgorithm
from amgs.algorithm.irrigation_algorithm import IrrigationAlgorithm


class Application:
    def __init__(self, config):
        self.config = config

        self.start_datetime = datetime.now()
        self.end_datetime = self.start_datetime + timedelta(seconds=self.config['runtime'])

        self.dht = AirSensor()
        self.ss = SoilSensor()

        self.fanset1 = FanRelay(1)
        self.fanset2 = FanRelay(2)
        self.pump = PumpRelay()
        self.light = LightRelay()

        self.airflow_alg = AirflowAlgorithm()
        self.irigation_alg = IrrigationAlgorithm()

        self.db = DBHandler('/home/jakebrown/final-year-project/src/database/database.db')

        self.camera = RPiCamera(self.config['cycle'])
    

    def mainloop(self):
        # main program loop
        while datetime.now() < self.end_datetime:
            # fetch sensor values and get path of photo
            path = self.fetch()
            
            # format fetched data and insert into database
            self.format(path)
            
            # compute actions for each sub-system
            irrigation, light, airflow = self.compute()
            
            # execute actions for each sub-system
            self.execute(irrigation, light, airflow)
            
            # sleep for interval
            time.sleep(self.config['interval'])

        # cleanup dht sensor on exit
        dht.cleanup()                    


    def fetch(self):
        self.dht.fetch()
        self.ss.fetch()

        if datetime.now() >= self.camera.next_ss_time:
            path = self.camera.take_snapshot()
            return path

        return None

    def format(self, path):
        air_data = {
            'temperature': self.dht.temp,
            'humidity': self.dht.humidity
        }

        soil_data = {
            'temperature': self.ss.temp,
            'moisture': self.ss.moisture
        }

        db.insert_data('air_data', air_data)
        db.insert_data('soil_data', soil_data)

        if path is not None:        
            photo_data = {
                'path': path            
            }

            db.insert_data('growth_snapshots', photo_data)


    def compute(self):
        if datetime.now() >= self.pump.next_activation:
            irrigation_action = self.irrigation_alg.compute(self.ss.temp, self.ss.moisture)


        if datetime.now().hour >= 18 or datetime.now().hour < 6:
            light_action = 'on'
        else:
            light_action = 'off'
    

        airflow_action = self.airflow_alg.compute(self.dht.temp, self.dht.humidity)

        return irrigation_action, light_action, airflow_action

    
    def execute(self, irrigation_action, light_action, airflow_action):
        if irrigation_action == 'short':
            duration = 3.0
        elif irrigation_action == 'medium':
            duration = 4.0
        else:
            duration = 5.0

        self.pump.set_state(True)
        time.sleep(duration)
        self.pump.set_state(False)


        if light_action == 'on':
            self.light.set_state(True)
        else:
            self.light.set_state(False)

        
        if airflow_action == 'off':
            fanset1.set_state(False)
            fanset2.set_state(False)

        elif airflow_action == 'half':
            fanset1.set_state(True)
            fanset2.set_state(False)

        else:
            fanset1.set_state(True)
            fanset2.set_state(True)