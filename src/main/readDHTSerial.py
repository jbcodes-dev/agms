from time import sleep
import serial
import dbhandler

# create database handler
DBHandler = dbhandler.DBHandler("/home/jakebrown/final-year-project/src/database/database.db")
DBHandler.create_connection()

# create serial connection
ser = serial.Serial('/dev/ttyACM0', 9600)


def main():
    while True:
        sleep(1)
        reading = ser.readline().decode()

        # if sensor didn't produce error
        if reading != "E":
            # value should be "T:H"
            reading = reading.split(":")
            data = {"temperature": reading[0], "humidity": reading[1]}
        
            # insert into table
            DBHandler.insert_data("DHT_data", data)

            # print table contents
            DBHandler.print_table("DHT_data")


if __name__ == "__main__":
    main()


