#include <Arduino.h>
#include <Arduino_HTS221.h>


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  if (!HTS.begin()) {
    Serial.println("Problemas para inicializar el sensor");
    while (1);
  }

  Serial.println("Sensor inicializado correctamente, empezando programa");
}

void loop() {
  // put your main code here, to run repeatedly:
  float temp = HTS.readTemperature();
  float hum = HTS.readHumidity();

  Serial.print("Temperatura: ");
  Serial.print(temp);
  Serial.print(" °C - Humedad: ");
  Serial.print(hum);
  Serial.println(" %");

  delay(1000);
}