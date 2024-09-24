#include <SPI.h>        // Library for SPI communication
#include <MFRC522.h>    // Library for RFID communication
#include <WiFi.h>       // Library for ESP32 WiFi connection
#include <HTTPClient.h> // Library for sending HTTP requests


#define SS_PIN 21  // SDA pin connected to GPIO 21
#define RST_PIN 22 // RST pin connected to GPIO 22


const char* ssid = "your_SSID";       // Replace with your WiFi network name
const char* password = "your_PASSWORD"; // Replace with your WiFi password


const String serverUrl = "http://192.168.31.195:3000/api/rfid"; // Replace with your server endpoint


void setup() {
  Serial.begin(115200); // Start serial communication for debugging
  SPI.begin();          // Initialize SPI bus
  rfid.PCD_Init();      // Initialize the RFID reader
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);        // Wait for WiFi connection
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}


void loop() {
  // Check if a new RFID tag is present and can be read
  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
    return;
  }

  // Read the UID from the RFID tag
  String uid = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    uid += String(rfid.uid.uidByte[i], HEX); // Convert the UID to a hex string
  }
  Serial.println("RFID Tag UID: " + uid);    // Print the UID to the serial monitor

  // Send the UID to the server via HTTP POST request
  if (WiFi.status() == WL_CONNECTED) {       // Ensure the ESP32 is still connected to WiFi
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Prepare the JSON request body
    String requestBody = "{\"uid\":\"" + uid + "\"}";
    int httpResponseCode = http.POST(requestBody); // Send the POST request

    if (httpResponseCode > 0) {
      String response = http.getString();     // Read the server's response
      Serial.println("Server Response: " + response);
    } else {
      Serial.println("Error in sending POST");
    }
    http.end();                              // End the HTTP connection
  }

  // Halt the RFID card to avoid multiple reads of the same card
  rfid.PICC_HaltA();
}
