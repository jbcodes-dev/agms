import terrarium
import dbhandler
import algorithm
import picam
import time
from datetime import datetime, timedelta


class App:
    def __init__(self, debug, cycle, control, cycle_length):
        self._debug = debug
        self._cycle = cycle
        self._control = control
        self._cycle_length = cycle_length

        if control:
            if self._debug:
                print("[DEBUG] starting in CONTROL mode")

            self._db = dbhandler.DBHandler("/home/jakebrown/final-year-project/src/database/database.db")
            self._camera = picam.PiCam("/home/jakebrown/final-year-project/snapshots/control")
            self._cycle_interval = 3600 # every hour take a photo

        else:
            if self._debug:
                print("[DEBUG] starting in NORMAL mode")

            self._terrarium = terrarium.Terrarium()
            self._db = dbhandler.DBHandler("/home/jakebrown/final-year-project/src/database/database.db")
            self._algorithm = algorithm.Algorithm()
            self._camera = picam.PiCam(f"/home/jakebrown/final-year-project/snapshots/cycle-{self._cycle}")
            self._cycle_interval = 30

        self._start_datetime = datetime.now()
        self._end_datetime = self._start_datetime + timedelta(seconds=self._cycle_length)

        if self._debug:
            print(f"[DEBUG] running for {self._cycle_length} seconds")


    def control_cycle(self):
        """ Control Cycle """
        
        if self._debug:
            print(f"[DEBUG] taking photo")
        
        # take photo on camera
        path = self._camera.take_snapshot()

        if self._debug:
            print(f"[DEBUG] snapshot at: {path}")

        # format data for db
        snapshot_data = {
            "path": path 
        }

        # insert to db
        self._db.insert_data("growth_snapshots", snapshot_data)
        
        if self._debug:
            print(f"[DEBUG] uploaded snapshot {path} to database")


    def main_cycle(self):
        """ Main Cycle """

        ### FETCH ###

        # fetch data from sensors and take snapshot
        self._terrarium.HumidityRegulation.HumiditySensor.fetch()
        self._terrarium.IrrigationSystem.SoilMoistureSensor.fetch()

        # take snapshot if it has been 1 hour
        if datetime.now() >= self._camera._next_snapshot_time:
            path = self._camera.take_snapshot()

        ### FORMAT ###
        # format sensor data
        air_data = {
            "air_temp": self._terrarium.HumidityRegulation.HumiditySensor.air_temperature,
            "air_humidity": self._terrarium.HumidityRegulation.HumiditySensor.humidity
        }

        soil_data = {
            "soil_temp": self._terrarium.IrrigationSystem.SoilMoistureSensor.soil_temperature,
            "soil_moisture": self._terrarium.IrrigationSystem.SoilMoistureSensor.soil_moisture
        }

        # format camera data
        snapshot_data = {
            "path": path 
        }


        ### UPLOAD ###
        # upload data to database
        self._db.insert_data("air_data", air_data)
        self._db.insert_data("soil_data", soil_data)
        self._db.insert_data("growth_snapshots", snapshot_data)

        """
        ### ALGORITHM
        # feed algorithm input variables
        # process inputs to get outputs
        # apply actions
        # cleanup algorithm
        
        # populate algorithm input variables
        self._algorithm.air_data = air_data
        self._algorithm.soil_data = soil_data
        # self._algorithm.light_data = light_data

        # process variables to get actions
        self._algorithm.process()

        # apply actions to relays
        self._terrarium.HumidityRegulation.AirflowRelay.change_relay_state(
            self._algorithm.actions["fans"]
        )

        
        if self._algorithm.actions["pump"]:
            self._terrarium.IrrigationSystem.WaterPumpRelay.change_relay_state(True)

            time.sleep(self._terrarium.IrrigationSystem.WaterPumpRelay.duration)



        self._terrarium.LightingSubsystem.LEDStripRelay.change_relay_state(
            self._algorithm.actions["light"]
        )

        # cleanup algorithm variables
        self._algorithm.cleanup()
        """
        
    def run(self):
        """ Program Loop """        

        if self._debug:
            print(f"[DEBUG] starting cycle-{self._cycle}")

        # will run for two weeks from start date
        while datetime.now() < self._end_datetime:
            # the control variable is set, only run the control cycle
            if self._control:
                self.control_cycle()

                if self._debug:
                    print(f"[DEBUG] sleeping for {self._cycle_interval} seconds")

                time.sleep(self._cycle_interval)

            # otherwise run main cycle
            else:
                self.main_cycle()
                
                if self._debug:
                    print(f"[DEBUG] sleeping for {self._cycle_interval} seconds")

                time.sleep(self._cycle_interval)
