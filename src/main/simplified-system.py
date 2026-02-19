import time
from datetime import datetime, timedelta

import board
import adafruit_dht
from adafruit_seesaw.seesaw import Seesaw

from picamzero import Camera

import dbhandler

import gpiozero as gpio



class AirSensor:
    def __init__(self):
        self.pin = board.D4
        self.temp = 0
        self.humidity = 0
        self.sensor = adafruit_dht.DHT22(self.pin)

    def fetch(self):
        self.temp = self.sensor.temperature
        self.humidity = self.sensor.humidity


class SoilSensor:
    def __init__(self):
        self.bus = board.I2C()
        self.temp = 0
        self.moisture = 0
        self.sensor = Seesaw(self.bus, addr=0x36)

    def fetch(self):
        self.moisture = self.sensor.moisture_read()
        self.temp = self.sensor.get_temp()


class PiCamera:
    def __init__(self, cycle_name):
        self.path = f"/home/jakebrown/final-year-project/snapshots/{cycle_name}/"
        self.camera = Camera()
        self.interval = 30 
        self.last_ss_time = None 
        self.next_ss_time = datetime.now() 
        self.ss_taken = 0

    def take_snapshot(self):
        location = f"{self.path}/{self.ss_taken + 1}.jpg"

        self.camera.still_size = (720, 360)
        self.camera.take_photo(location)

        self.ss_taken += 1

        self.last_ss_time = datetime.now()
        self.next_ss_time = self.last_ss_time + timedelta(seconds=self.interval)

        return location


def main():
    # cycle config
    config = {
        "runtime": 300,
        "interval": 30,
        "cycle": "test",
        "run_alg": False,
        "debug": True,
    }

    # set start and end times
    start_datetime = datetime.now()
    end_datetime = start_datetime + timedelta(seconds=config["runtime"])

    # setup
    dht = AirSensor()
    ss = SoilSensor()
    db = dbhandler.DBHandler("/home/jakebrown/final-year-project/src/database/database.db")
    camera = PiCamera(config["cycle"])

    if config["debug"]:
        print(f"""
[DEBUG]: ({datetime.now()}) {config['cycle']} cycle started with parameters:
    runtime: {config['runtime']}s
    interval: {config['interval']}s
    run_alg: {config['run_alg']}
    debug: {config['debug']}""")

    # mainloop
    while datetime.now() < end_datetime:

        # fetch
        dht.fetch()
        ss.fetch()

        if config["debug"]:
            print(f"[DEBUG] ({datetime.now()}) air data fetched: T: {dht.temp} / H: {dht.humidity}")
            print(f"[DEBUG] ({datetime.now()}) soil data fetched: T: {ss.temp} / M: {ss.moisture}")


        # format
        air_data = {
            "temperature": dht.temp,
            "humidity": dht.humidity
        }

        soil_data = {
            "temperature": ss.temp,
            "moisture": ss.moisture
        }

        # upload
        db.insert_data("air_data", air_data)
        db.insert_data("soil_data", soil_data)

        # capture and get path if time correct
        if datetime.now() >= camera.next_ss_time:
            path = camera.take_snapshot()
            
            ss_data = {
                "path": path
            }

            db.insert_data("growth_snapshots", ss_data)

            # print debug msg
            if config["debug"]:
                print(f"[DEBUG] ({datetime.now()}) snapshot taken at {path}")

        # algorithm goes here

        # update relays here

        # sleep for interval
        if config["debug"]:
            print(f"[DEBUG] ({datetime.now()}) sleeping for {config['interval']} seconds")

        time.sleep(config["interval"])

    
    # on exit
    dht.sensor.exit()

    
if __name__ == "__main__":
    main()

