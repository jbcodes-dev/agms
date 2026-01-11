from terrarium import Terrarium


def main():
    terrarium = Terrarium()

    for sub_entry in terrarium.subsystems:
        print(sub_entry)

        for mod_entry in terrarium.subsystems[sub_entry].modules:
            print(f"Module Name: {terrarium.subsystems[sub_entry].modules[mod_entry].name}\nModule Desc: {terrarium.subsystems[sub_entry].modules[mod_entry].desc}")


    while True:

        ### FETHCH ###

        # temp humidity
        


if __name__ == "__main__":
    main()



# mainloop

"""

fetch:
    get temp_humidity reading
    get soil_moisture reading
    get time of day
    
    send to database

decode:
    temp_humidity > some_value ? airflow=true : airflow=false
    soil_moisture < some_value ? irrigation=true : irrigation=false # how long is determined by how low the value is in algorithm.py
    17.59 < time_of_day < 5.59 ? lighting=true : lighting=false

execute:
    set airflow=value
    set irrigation=value
    set lighting=value

"""
