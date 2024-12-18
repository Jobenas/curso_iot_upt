#include <Arduino.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFi.h>
#include <ESP32Time.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <esp_wifi.h>


#define DHTPIN 4
#define DHTTYPE DHT11
#define SAMPLE_WINDOW 1000    // en ms
#define CALC_WINDOW 10000     // en ms
#define SAMPLE_WINDOW_SECS 1  // en segundos
#define CALC_WINDOW_SECS 10   // en segundos
#define MAX_SAMPLES 10

#define BROKER_URL "test.mosquitto.org"


DHT_Unified dht(DHTPIN, DHTTYPE);

uint32_t sampleWindowStart, calcWindowStart;

float samples[MAX_SAMPLES] = {0};
uint8_t sampleIdx = 0;

const char* ssid = ""; // SSID
const char* password = ""; // Password

const char* brokerUrl = "test.mosquitto.org";

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

ESP32Time rtc(0); // UTC

JsonDocument payload;

WiFiUDP ntpUDP;

uint8_t baseMac[6];

NTPClient timeClient(ntpUDP, "0.south-america.pool.ntp.org", 0, 60000);

void reconnect(void) {
  // Loop until we're reconnected
  while (!mqttClient.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP32-Temp";
    // Attempt to connect
    if (mqttClient.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void readMacAddress(){
  esp_err_t ret = esp_wifi_get_mac(WIFI_IF_STA, baseMac);
  if (ret == ESP_OK) {
    Serial.printf("%02x:%02x:%02x:%02x:%02x:%02x\n",
                  baseMac[0], baseMac[1], baseMac[2],
                  baseMac[3], baseMac[4], baseMac[5]);
  } else {
    Serial.println("Failed to read MAC address");
  }
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  dht.begin();

  payload["promedio"] = 0;
  payload["maximo"] = 0;
  payload["minimo"] = 0;
  payload["mediana"] = 0;

  WiFi.begin(ssid, password);

  Serial.print("Intentando conectar a la red WiFi.");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("Conectado a la red WiFi!");

  mqttClient.setServer(brokerUrl, 1883);
  readMacAddress();
  timeClient.begin();
  timeClient.update();
  rtc.setTime(timeClient.getEpochTime());
  sampleWindowStart = rtc.getEpoch();
  calcWindowStart = rtc.getEpoch();
}

void loop() {
  // put your main code here, to run repeatedly:
  if(!mqttClient.connected()) {
    reconnect();
  }

  mqttClient.loop();

  if((rtc.getEpoch() - sampleWindowStart) >= SAMPLE_WINDOW_SECS) {
    sensors_event_t event;

    dht.temperature().getEvent(&event);
    float temp = event.temperature;
    samples[sampleIdx] = temp;
    sampleIdx++;

    sampleWindowStart = rtc.getEpoch();

    Serial.println(rtc.getTime("%Y-%m-%d %H:%M:%S"));
    Serial.print("Epoch: ");
    Serial.println(rtc.getEpoch());
  }

  if((rtc.getEpoch() - calcWindowStart) >= CALC_WINDOW_SECS) {
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
    payload["timestamp"] = rtc.getTime("%Y-%m-%d %H:%M:%S");
    String devId = String(baseMac[0], HEX) + String(baseMac[1], HEX) + String(baseMac[2], HEX) + String(baseMac[3], HEX) + String(baseMac[4], HEX) + String(baseMac[5], HEX);
    payload["device_id"] = devId;

    String payloadStr;

    serializeJson(payload, payloadStr);
    Serial.println(payloadStr);
    sampleIdx = 0;
    calcWindowStart = rtc.getEpoch();
    
    mqttClient.publish("/upt/curso_iot/ESP32-Temp", payloadStr.c_str());
  }
}

