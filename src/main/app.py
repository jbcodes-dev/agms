import terrarium
import dbhandler
import algorithm


class App:
    def __init__(self, debug):
        self._debug = debug
        self._terrarium = terrarium.Terrarium()
        self._db = dbhandler.DBHandler("src/database/database.db")
        self._algorithm = algorithm.Algorithm()


    def run(self):
        """ Main Program Loop """        

        while True:
            # TODO: separate this into private methods
            # TODO: add try-except statements to manage errors

            # fetch data from sensors
            self._terrarium.HumidityRegulation.HumiditySensor.fetch()
            self._terrarium.IrrigationSystem.SoilMoistureSensor.fetch()

            # format data
            air_data = {
                "air_temp": self._terrarium.HumidityRegulation.HumiditySensor.air_temperature,
                "air_humidity": self._terrarium.HumidityRegulation.HumiditySensor.air_humidity
            }

            soil_data = {
                "soil_temp": self._terrarium.IrrigationSystem.SoilMoistureSensor.soil_temperature,
                "soil_moisture": self._terrarium.IrrigationSystem.SoilMoistureSensor.soil_moisture
            }

            # upload data to database
            self._db.insert_data("air_data", air_data)
            self._db.insert_data("soil_data", soil_data)


            ### ALGORITHM ###

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

            self._terrarium.IrrigationSystem.WaterPumpRelay.change_relay_state(
                self._algorithm.actions["pump"]
            )

            self._terrarium.LightingSubsystem.LEDStripRelay.change_relay_state(
                self._algorithm.actions["light"]
            )

            # cleanup algorithm variables
            self._algorithm.cleanup()