import time
from datetime import datetime, timedelta

import board
import adafruit_dht
from adafruit_seesaw.seesaw import Seesaw

from picamzero import Camera

import dbhandler

import gpiozero



class AirSensor:
    def __init__(self):
        self.pin = board.D4
        self.temp = 0
        self.humidity = 0
        self.sensor = adafruit_dht.DHT22(self.pin)

    def fetch(self):
        # TODO: put in error catch method here to prevent crashing
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


class LEDRelay:
    def __init__(self):
        self.pin = 9
        self.state = False
        self.relay = gpiozero.OutputDevice(self.pin, active_high=False, initial_value=False)
        self.relay.off()
        
    def set_state(self, new_state):
        self.state = new_state

        if self.state:
            self.relay.on()

        else:
            self.relay.off()


class PumpRelay:
    def __init__(self):
        self.pin = 10
        self.state = False
        self.relay = gpiozero.OutputDevice(self.pin, active_high=False, initial_value=False)
        self.relay.off()

    def set_state(self, new_state):
        self.state = new_state
        
        if self.state:
            self.relay.on()

        else:
            self.relay.off()


class FanG1Relay:
    def __init__(self):
        self.pin = 23
        self.state = False
        self.relay = gpiozero.OutputDevice(self.pin, active_high=False, initial_value=False)
        self.relay.off()

    def set_state(self, new_state):
        self.state = new_state

        if self.state:
            self.relay.on()

        else:
            self.relay.off()


class FanG2Relay:
    def __init__(self):
        self.pin = 24
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

    # setup sensors
    dht = AirSensor()
    ss = SoilSensor()

    # setup relays
    fanset1 = FanG1Relay()
    fanset2 = FanG2Relay()
    pump = PumpRelay()
    light = LEDRelay()

    # setup database handler
    db = dbhandler.DBHandler("/home/jakebrown/final-year-project/src/database/database.db")
    
    # setup camera
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
        # basic algorithm

        # set light relay
        if datetime.now().hour >= 18 or datetime.now().hour < 6:
            light.set_state(True)
        
        else:
            light.set_state(False)

        
        # set pump relay
        # need to do something with a timer based on the last pump activation time
        # will be similar to the camera timer implementation, just longer

        
        # set fan relay
        # if temp and humidity are more than optimum, activate both relays
        # if temp < 18 turn off fan, if temp > 18 and < 24 turn on one fan
        # if humidity < 45 turn off fan, if humidity > 45 and < 70 turn on one fan

        if dht.temp < 18.0 and dht.humidity < 45.0:
            fanset1.set_state(False)
            fanset2.set_state(False)

        elif 18.0 < dht.temp < 24.0 and 45.0 < dht.humidity < 70.0:
            fanset1.set_state(True)
            fanset2.set_state(False)

        elif dht.temp > 24.0 or dht.humidity > 70.0:
            fanset1.set_state(True)
            fanset2.set_state(True)

        
        if config["debug"]:
            print(f"[DEBUG] ({datetime.now()}) fanset1: {fanset1.state} | {fanset2.state}")
            print(f"[DEBUG] ({datetime.now()}) light: {light.state}")


        # sleep for interval
        if config["debug"]:
            print(f"[DEBUG] ({datetime.now()}) sleeping for {config['interval']} seconds")

        time.sleep(config["interval"])

    
    # on exit
    dht.sensor.exit()

    
if __name__ == "__main__":
    main()

