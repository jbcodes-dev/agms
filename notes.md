# Notes

Rule-Based Fuzzy Algorithm:

- Normalise the database values for temperature and humidity
- Define the fuzzy member sets for temperature and humidity

Timer-Based Activation Algorithm:

- Variables: Interval (seconds), Duration (seconds), LastActivationTime (time), NextActivationTime (LastActivationTime + Interval)
- Activate the water pump relay based on a timer, if the timer has reached zero, activate the water pump for the duration and reset the timer.

Time-of-Day-Based Activation Algorithm:

- Variables: TimeToActivate (hh:mm:ss), TimeToDeactivate (hh:mm:ss)
- Activate the light relay at TimeToActivate, deactivate the light relay at TimeToDeactivate.

Fuzzy Algorithm for fan activation:

- Normalise the database values.
- Define sets for temperature, humidity, and fan count.
- Fuzzify inputs.
- Process inputs through rule table.
- Inference
- Defuzzify outputs

Water the plants every few hours, turning the pump on for x seconds to dispense x ml of water.
The pump will water the bottom of the tank, preventing mold from forming on the leaves of the microgreens.

IF air_temp IS < 18 THEN air_temp = LOW
IF air_temp IS > 18 AND < 22 THEN air_temp = MED
IF air_temp IS > 22 THEN air_temp = HIGH

IF air_humidity IS < 50 THEN air_humidity = LOW
IF air_humidity IS > 50 AND < 70 THEN air_humidity = MED
IF air_humidity IS > 70 THEN air_humidity = HIGH

fan settings: none, 2, 4, 6, all
