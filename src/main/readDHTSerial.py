from time import sleep
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
    sleep(1)
    val = ser.readline()
    print(val)
