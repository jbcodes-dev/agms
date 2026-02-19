import time
import board

from adafruit_seesaw.seesaw import Seesaw
import adafruit_dht


i2c_bus = board.I2C()
dht_pin = board.D4

ss = Seesaw(i2c_bus, addr=0x36)
dht = adafruit_dht.DHT22(dht_pin)

while True:
    soil_moisture = ss.moisture_read()
    soil_temp = ss.get_temp()

    air_temp = dht.temperature
    air_humidity = dht.humidity

    print(f"SOIL// {str(soil_temp)} / M: {str(soil_moisture)}")
    print(f" AIR// T: {str(air_temp)} / H: {str(air_humidity)}\n")


    time.sleep(5)
