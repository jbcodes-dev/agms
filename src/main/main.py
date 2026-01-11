from terrarium import Terrarium
from dbhandler import DBHandler


def main():
    t = Terrarium()
    db = DBHandler("src/database/database.db")

    """
    for sub_entry in terrarium.subsystems:
        print(sub_entry)

        for mod_entry in terrarium.subsystems[sub_entry].modules:
            print(f"Module Name: {terrarium.subsystems[sub_entry].modules[mod_entry].name}\nModule Desc: {terrarium.subsystems[sub_entry].modules[mod_entry].desc}")
    """

    while True:

        ### FETCH ###

        t.HumidityRegulation.HumiditySensor.fetch()
        t.IrrigationSystem.SoilMoistureSensor.fetch()

        ### FORMAT ###

        air_data = {
            "temperature": t.HumidityRegulation.HumiditySensor.temperature,
            "humidity": t.HumidityRegulation.HumiditySensor.humidity
            }
        
        soil_data = {
            "temperature": t.IrrigationSystem.SoilMoistureSensor.soil_temperature,
            "moisture": t.IrrigationSystem.SoilMoistureSensor.soil_moisture
        }

        ### UPLOAD ###

        db.insert_data("DHT_data", air_data)
        # dbhandler.insert_data("soil_data", soil_data)

        ### ALGORITHM ###

        # AIRFLOW
        # if air_temp < 18.0 and air_humidity < 50.0
        #   turn off fan relay
        
        # elif air_temp > 22.0 and air_humidity > 70.0
        #   turn on fan relay

        # WATER PUMP
        # if soil_moisture < 30.0
        #   turn on water pump relay
        
        # elif soil_moisture > 50.0
        #   turn off water pump relay

        # LIGHTING
        # if 06:00 < current_time < 17.59
        #   turn off lighting relay

        # elif 06:00 > current_time > 17:59
        #   turn on lighting relay
        
        """
        In future, the algorithm to engage each relay will go through a separate class to be more indepth
        and optimised.

        Each action the algorithm takes will be logged in a text file.
        """

        ### EXECUTE ###

        # based on algorithm class decisions, modify relay behaviour accordingly


if __name__ == "__main__":
    main()
