#include <Wire.h>
#include <Adafruit_INA219.h>
#include "DHT.h"

// Constants
#define DHTPIN 7        // Pin for DHT sensor
#define DHTTYPE DHT22   // or DHT11 depending on your sensor

// Initialize sensor objects
DHT dht(DHTPIN, DHTTYPE);
Adafruit_INA219 ina219;

// Variables for data storage
float solarVoltage, solarCurrent, solarPower;
float temperature, humidity;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  
  // Initialize DHT sensor
  dht.begin();
  
  // Initialize INA219 sensor
  if (!ina219.begin()) {
    Serial.println("Failed to find INA219 chip. Check wiring!");
    while (1) { delay(10); }
  }

  Serial.println("Solar Panel Data Acquisition System Initialized!");
}

void loop() {
  // 1. Read solar voltage/current/power
  solarVoltage = ina219.getBusVoltage_V();      // Volts
  solarCurrent = ina219.getCurrent_mA() / 1000.0; // mA to A
  solarPower   = ina219.getPower_mW() / 1000.0;   // mW to W

  // 2. Read temperature & humidity
  temperature = dht.readTemperature();
  humidity    = dht.readHumidity();

  // 3. Check for failed readings
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
  }

  // 4. Output to Serial Monitor
  Serial.println("==================================");
  Serial.print("Solar Voltage (V): "); Serial.println(solarVoltage);
  Serial.print("Solar Current (A): "); Serial.println(solarCurrent);
  Serial.print("Solar Power   (W): "); Serial.println(solarPower);
  Serial.print("Temperature (°C): ");  Serial.println(temperature);
  Serial.print("Humidity    (%): ");  Serial.println(humidity);
  Serial.println("==================================\n");

  delay(2000);  // Wait 2 seconds
}
