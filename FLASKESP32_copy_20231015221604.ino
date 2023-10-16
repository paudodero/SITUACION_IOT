#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DFRobot_DHT11.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <MQ135.h>
#include <Ds1302.h>

// Instanciar objetos y definir pines
#define DHT11_PIN 27
#define MQ135_PIN 35
#define PIN_CLK 26
#define PIN_DAT 25
#define PIN_RST 18

//MQ135 gasSensor(MQ135_PIN);
LiquidCrystal_I2C lcd(0x27, 16, 2);
DFRobot_DHT11 DHT;
Ds1302 rtc(PIN_RST, PIN_CLK, PIN_DAT);
String date_time;


const int buttonPin1 = 33;
const int buttonPin2 = 14;
int displayMode = 0; // 0: Temp, 1: Humidity, 2: Gas, 3: Time
const char* ssid = "Tec-Contingencia";
const char* password = "";
const char* apiEndpoint = "https://ominous-giggle-69g47p969jjjc4wrx-5000.app.github.dev/sensor_data";

const static char* WeekDays[] = {
    "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
};

void setupWifi() {
    Serial.begin(9600);
    Serial.print("Connecting to WiFi");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }
    Serial.print(" Connected: ");
    Serial.println(WiFi.localIP());
}


void setup() {
  lcd.init(); // Pass your I2C address as an argument if it's not the default
  lcd.backlight();
  Serial.begin(115200);
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);
  rtc.init();

  Ds1302::DateTime now;
    rtc.getDateTime(&now);
    String date_time = "20" + String(now.year) + "-" + 
                      ((now.month < 10) ? "0" : "") + String(now.month) + "-" + 
                      ((now.day < 10) ? "0" : "") + String(now.day) + " " +
                      ((now.hour < 10) ? "0" : "") + String(now.hour) + ":" + 
                      ((now.minute < 10) ? "0" : "") + String(now.minute) + ":" + 
                      ((now.second < 10) ? "0" : "") + String(now.second);
    setupWifi();
}

void sendData(float temperature, float humidity, int mq135Value, String date_time) {
    Serial.print("Sending data to API: ");

    HTTPClient http;
    http.begin(apiEndpoint);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<300> doc;

    doc["temperature"] = temperature;
    doc["humidity"] = humidity;
    doc["mq135Value"] = mq135Value;
    doc["date_time"] = date_time;

    String json;
    serializeJson(doc, json);
    Serial.println("Sending JSON: " + json);

    int httpResponseCode = http.POST(json);
    if (httpResponseCode > 0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        String responseString = http.getString();
        Serial.println("Received response: " + responseString);

        // Aquí puedes agregar lógica adicional según la respuesta del servidor
        // Por ejemplo, verificar si la solicitud fue exitosa, etc.
    } else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);

        // Aquí puedes agregar manejo de errores, como intentar nuevamente o notificar problemas.
    }
    http.end();
}



void loop() {
  // Tu código para el manejo de los botones y sensores aquí
lcd.clear();
Ds1302::DateTime now;
rtc.getDateTime(&now);

String date_time = "20" + String(now.year) + "-" + 
                  ((now.month < 10) ? "0" : "") + String(now.month) + "-" + 
                  ((now.day < 10) ? "0" : "") + String(now.day) + " " +
                  ((now.hour < 10) ? "0" : "") + String(now.hour) + ":" + 
                  ((now.minute < 10) ? "0" : "") + String(now.minute) + ":" + 
                  ((now.second < 10) ? "0" : "") + String(now.second);

    DHT.read(DHT11_PIN);
    float temperature = DHT.temperature;
    float humidity = DHT.humidity;

    int mq135Value = analogRead(MQ135_PIN) / 100;


    // El resto de tu función sendData permanece igual

  if (digitalRead(buttonPin1) == LOW && digitalRead(buttonPin2) == LOW) {
    DHT.read(DHT11_PIN);
    lcd.setCursor(0, 0);
    lcd.print("Temp:");
    lcd.print(temperature);
  } 
  else if (digitalRead(buttonPin1) == HIGH && digitalRead(buttonPin2) == LOW) {
    DHT.read(DHT11_PIN);
    lcd.setCursor(0, 0);
    lcd.print("Humi: ");
    lcd.print(humidity);
    lcd.print("%");
  } 
  else if (digitalRead(buttonPin1) == LOW && digitalRead(buttonPin2) == HIGH) {
    lcd.setCursor(0, 0);
    lcd.print("CO2 (PPM): ");
    lcd.print(mq135Value);
  } 
  else if (digitalRead(buttonPin1) == HIGH && digitalRead(buttonPin2) == HIGH) {
  lcd.print(date_time);
  }
sendData(temperature,humidity,mq135Value,date_time);
  delay(2000); // Ajusta este delay según tus necesidades
}


