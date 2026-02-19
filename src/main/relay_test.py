import time

import gpiozero

RED_LED_PIN = 23
GREEN_LED_PIN = 24
BLUE_LED_PIN = 10
YELLOW_LED_PIN = 9

# set pins
# pins = [16, 18, 19, 21]
pins = [23, 24, 10, 9]

# setup relays
relay_red = gpiozero.OutputDevice(RED_LED_PIN, active_high=False, initial_value=False)
relay_green = gpiozero.OutputDevice(GREEN_LED_PIN, active_high=False, initial_value=False)
relay_blue = gpiozero.OutputDevice(BLUE_LED_PIN, active_high=False, initial_value=False)
relay_yellow = gpiozero.OutputDevice(YELLOW_LED_PIN, active_high=False, initial_value=False)


# turn all relays off
relay_red.off()
relay_green.off()
relay_blue.off()
relay_yellow.off()


# test red relay
# print(f"red: {relay_red.value}")
# time.sleep(3)
# relay_red.on()
# print(f"red: {relay_red.value}")
# time.sleep(3)
# relay_red.off()


# test multiple relays - red, yellow, green, blue
time.sleep(3)
relay_red.on()
time.sleep(3)
relay_green.on()
time.sleep(3)
relay_blue.on()
time.sleep(3)
relay_yellow.on()

# turn them off
time.sleep(3)
relay_red.off()
time.sleep(3)
relay_green.off()
time.sleep(3)
relay_blue.off()
time.sleep(3)
relay_yellow.off()
time.sleep(3)
