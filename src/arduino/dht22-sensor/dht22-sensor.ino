#include <DHT.h>

#define DHT22_PIN 2

DHT dht(DHT22_PIN, DHT22);

void setup() {
	Serial.begin(9600);

 dht.begin();
}

void loop() {
  delay(2000);
  
	float h = dht.readHumidity();
	float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.print("Failed to read.\n");
    return;
  }

	Serial.print("H: ");
	Serial.print(h);

	Serial.print(" | T: ");
	Serial.print(t);
  Serial.print("\n");
}
