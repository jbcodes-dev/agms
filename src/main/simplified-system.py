import time
from datetime import datetime, timedelta

from air_sensor import AirSensor
from soil_sensor import SoilSensor
from rpi_camera import RPiCamera

from light_relay import LightRelay

import dbhandler

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
    light = LightRelay()

    # setup database handler
    db = dbhandler.DBHandler("/home/jakebrown/final-year-project/src/database/database.db")
    
    # setup camera
    camera = RPiCamera(config["cycle"])


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

        # basic algorithm
        # in future: algorithm will be optimised by including more advanced algorithms such as PID and Rule-based fuzzy inference


        # due to the power draw of running a water pump, we will take care of the watering first to ensure the process has finished
        # in order to free up power for the remaining systems.

        # activate pump for 3 seconds to see how much water is moved
        # test as part of the system to understand power draw
        if datetime.now() >= pump.next_activation:
            pump.set_state(True)

            if config["debug"]:
                print(f"[DEBUG] ({datetime.now()})  pump: {pump.state}")

            time.sleep(2.5)
            pump.set_state(False)

            if config["debug"]:
                print(f"[DEBUG] ({datetime.now()})  pump: {pump.state}")


        # set light relay
        # turn on light if time is between 6pm and 6am
        if datetime.now().hour >= 18 or datetime.now().hour < 6:
            light.set_state(True)
        
        else:
            light.set_state(False)


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
            print(f"[DEBUG] ({datetime.now()})  fans: {fanset1.state} | {fanset2.state}")
            print(f"[DEBUG] ({datetime.now()}) light: {light.state}")


        # sleep for interval
        if config["debug"]:
            print(f"[DEBUG] ({datetime.now()}) sleeping for {config['interval']} seconds")

        time.sleep(config["interval"])

    
    # on exit
    dht.cleanup()

    
if __name__ == "__main__":
    main()

