#include <Arduino.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>

#define DHTPIN 4
#define DHTTYPE DHT11
#define SAMPLE_WINDOW 1000    // en ms
#define CALC_WINDOW 10000     // en ms
#define MAX_SAMPLES 10

#define BROKER_URL "test.mosquitto.org"


DHT_Unified dht(DHTPIN, DHTTYPE);

uint32_t sampleWindowStart, calcWindowStart;

float samples[MAX_SAMPLES] = {0};
uint8_t sampleIdx = 0;

JsonDocument payload;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  dht.begin();

  sampleWindowStart = millis();
  calcWindowStart = millis();

  payload["promedio"] = 0;
  payload["maximo"] = 0;
  payload["minimo"] = 0;
  payload["mediana"] = 0;
}

void loop() {
  // put your main code here, to run repeatedly:
  if((millis() - sampleWindowStart) >= SAMPLE_WINDOW) {
    sensors_event_t event;

    dht.temperature().getEvent(&event);
    float temp = event.temperature;
    samples[sampleIdx] = temp;
    sampleIdx++;

    sampleWindowStart = millis();
  }

  if((millis() - calcWindowStart) >= CALC_WINDOW) {
    float sum = 0;
    for(uint8_t i = 0; i < MAX_SAMPLES; i++) {
      sum += samples[i];
    }
    float avg = sum / MAX_SAMPLES;

    
    // ordenar para obtener maximo minimo y mediana (bubble sort)
    for(uint8_t i = 0; i < MAX_SAMPLES; i++) {
      for(uint8_t j = i + 1; j < MAX_SAMPLES; j++) {
        if(samples[i] > samples[j]) {
          float aux = samples[i];
          samples[i] = samples[j];
          samples[j] = aux;
        }
      }
    }

    float tempMax = samples[MAX_SAMPLES - 1];
    float tempMin = samples[0];
    float tempMediana = samples[MAX_SAMPLES / 2];

    payload["promedio"] = avg;
    payload["maximo"] = tempMax;
    payload["minimo"] = tempMin;
    payload["mediana"] = tempMediana;
    payload["unidad"] = "°C";

    String payloadStr;

    serializeJson(payload, payloadStr);
    Serial.println(payloadStr);
    sampleIdx = 0;
    calcWindowStart = millis(); 
  }
}

