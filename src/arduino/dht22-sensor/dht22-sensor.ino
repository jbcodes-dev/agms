#include <DHT.h>

#define DHT22_PIN 2

DHT dht(DHT22_PIN, DHT22);

void setup() {
	Serial.begin(9600);

 dht.begin();
}

void loop() {
  delay(2000);
  
	float t = dht.readTemperature();
	float h = dht.readHumidity();

  if (isnan(h) || isnan(t)) {
    Serial.print("E\n");
    return;
  }

	Serial.print(t);
	Serial.print(":");
	Serial.print(h);
  Serial.print("\n");
}
