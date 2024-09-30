#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <HTTPClient.h>

#define SS_PIN 5    // SDA/SS pin connected to GPIO 5
#define RST_PIN 22  // RST pin connected to GPIO 22

MFRC522 rfid(SS_PIN, RST_PIN); // Create instance of MFRC522 class
MFRC522::MIFARE_Key key;       // Create MIFARE_Key structure to hold security key

// WiFi Credentials
const char* ssid = "Galaxy M33 5G";
const char* password = "aju12345";

// Server URL for POST request
const String serverUrl = "http://192.168.235.249:3000/api/rfid";

void setup() { 
  Serial.begin(115200);         // Initialize serial communications
  SPI.begin(18, 19, 23);        // Initialize SPI bus with SCK, MISO, and MOSI pins
  rfid.PCD_Init();              // Initialize the RFID reader

  // Set all key bytes to 0xFF for default authentication key
  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }

  Serial.println(F("Scanning MIFARE Classic NUID for Entry"));

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);  // Wait for WiFi connection
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  // Reset the loop if no new card is present on the reader
  if (!rfid.PICC_IsNewCardPresent())
    return;

  // Check if the NUID has been read
  if (!rfid.PICC_ReadCardSerial())
    return;

  // Read the UID from the RFID tag
  String uid = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    uid += String(rfid.uid.uidByte[i], HEX); // Convert the UID to a hex string
  }
  Serial.println("RFID Tag UID: " + uid);    // Print the UID to the serial monitor

  // Since we only handle entry, we set the entryType to "Entry"
  String entryType = "Entry";

  // Send the UID and entry_type to the server via HTTP POST request
  sendRfidData(uid, entryType);

  // Halt the RFID card to avoid multiple reads of the same card
  rfid.PICC_HaltA();

  // Stop encryption on PCD (RFID reader)
  rfid.PCD_StopCrypto1();
}

/**
 * Send the UID and entry_type to the server via HTTP POST request.
 */
void sendRfidData(String uid, String entryType) {
  if (WiFi.status() == WL_CONNECTED) {  // Ensure the ESP32 is connected to WiFi
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Prepare the JSON request body
    String requestBody = "{\"uid\":\"" + uid + "\", \"entry_type\":\"" + entryType + "\"}";
    Serial.println("Sending data to server: " + requestBody);

    // Send the POST request
    int httpResponseCode = http.POST(requestBody);

    // Check the response from the server
    if (httpResponseCode > 0) {
      String response = http.getString();  // Read the server's response
      Serial.println("Server Response: " + response);

      // Check if the response indicates a conflict (entry already exists)
      if (httpResponseCode == 409) {
        Serial.println("Conflict: " + response); // Entry already exists
      } else {
        Serial.println("Data sent successfully."); // Successful entry
      }
    } else {
      Serial.println("Error in sending POST: " + String(httpResponseCode));
    }

    http.end();  // End the HTTP connection
  } else {
    Serial.println("WiFi not connected, unable to send data.");
  }
}

/**
 * Helper function to print a byte array as hex values to the Serial monitor.
 */
void printHex(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
  Serial.println();
}

/**
 * Helper function to print a byte array as decimal values to the Serial monitor.
 */
void printDec(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(' ');
    Serial.print(buffer[i], DEC);
  }
  Serial.println();
}
