#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <map>  // Include the map library

// RFID Module Pins
#define RST_PIN 22
#define SS_PIN 5

MFRC522 rfid(SS_PIN, RST_PIN); // Create instance of MFRC522 for RFID

// WiFi Credentials
const char* ssid = "Galaxy M33 5G 0C47";
const char* password = "aju12345";

// Backend API URL
const char* serverUrl = "http://192.168.248.249:3000/api/rfid";
const char* checkUidUrl = "http://192.168.248.249:3000/api/rfid/check-uid";

// Cooldown timer
unsigned long lastScanTime = 0; // Tracks the last scan time
const unsigned long cooldownTime = 3000; // 3 seconds cooldown

// To track the state of each UID (Entry or Exit)
String entryType = "Entry"; // Default to Entry on the first scan
String location = "Warehouse 1"; // You can dynamically update this based on your setup

// Map to track scan counts for each card UID (Entry and Exit are toggled)
std::map<String, int> cardScanCount;  // Key: UID, Value: scan count

void setup() {
  Serial.begin(115200); // Initialize Serial for debugging

  // Initialize RFID
  SPI.begin(); // Start the SPI bus
  rfid.PCD_Init(); // Initialize the MFRC522 RFID module
  if (!rfid.PCD_PerformSelfTest()) { // Check if RFID is properly initialized
    Serial.println("RFID initialization failed. Check wiring.");
    while (true); // Halt execution if RFID fails to initialize
  }
  Serial.println("RFID Reader Initialized");

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
}

// Function to check the current entry type of the UID from the backend
String getEntryTypeFromServer(String uid) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(checkUidUrl); // Begin HTTP request to check UID entry type
    http.addHeader("Content-Type", "application/json"); // Set content type to JSON

    // Create JSON payload with UID
    String payload = String("{\"uid\":\"") + uid + "\"}";
    Serial.println("Sending payload to check entry type: " + payload);
    
    int httpResponseCode = http.POST(payload); // Send POST request
    String entryType = "Entry"; // Default to Entry if not found or error occurs

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Server Response: " + response);

      // Parse response and set entryType
      if (response.indexOf("Entry") != -1) {
        entryType = "Entry";
      } else if (response.indexOf("Exit") != -1) {
        entryType = "Exit";
      }
    } else {
      Serial.println("Error checking entry type. HTTP Response: " + String(httpResponseCode));
    }
    http.end(); // End the HTTP request
    return entryType;
  } else {
    Serial.println("WiFi not connected. Cannot check entry type.");
    return "Entry"; // Default to Entry if WiFi is not connected
  }
}

void loop() {
  // Ensure there's a cooldown between scans
  if (millis() - lastScanTime < cooldownTime) {
    return; // Skip reading if cooldown has not passed
  }

  // Check if a new RFID card is present
  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
    return; // If no card detected, skip further execution
  }

  // Read RFID tag UID and convert it to a string
  String uid = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    uid += String(rfid.uid.uidByte[i], HEX);
    if (i != rfid.uid.size - 1) {
      uid += "-"; // Add hyphen between bytes for readability
    }
  }
  uid.toUpperCase(); // Ensure UID is in uppercase for consistency
  Serial.println("Tag UID: " + uid);

  // Query the server for the entry type (Entry/Exit) of the UID
  String currentEntryType = getEntryTypeFromServer(uid);

  // Track scan count for the card UID
  if (cardScanCount.find(uid) != cardScanCount.end()) {
    cardScanCount[uid]++; // Increment scan count for an existing card
  } else {
    cardScanCount[uid] = 1; // Initialize scan count for the card
  }

  // Update entry type based on server data
  if (cardScanCount[uid] == 1 && currentEntryType == "Entry") {
    entryType = "Entry"; // First scan, Entry
    Serial.println("Card Entry: " + uid);
  } else if (cardScanCount[uid] == 2 && currentEntryType == "Entry") {
    entryType = "Exit"; // Second scan, Exit
    Serial.println("Card Exit: " + uid);
  } else {
    // If the entry type does not match the current scan (already processed)
    Serial.println("Card already used: " + uid);
    return;  // Do not send data for third or more scans
  }

  // Update the last scan time to implement cooldown
  lastScanTime = millis();

  // Send UID, entry type, and location to the backend server
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl); // Begin HTTP request to backend
    http.addHeader("Content-Type", "application/json"); // Set content type to JSON

    // Create JSON payload with UID, entry type, and location
    String payload = String("{\"uid\":\"") + uid + String("\",\"entry_type\":\"") + entryType + String("\",\"location\":\"") + location + "\"}";
    Serial.println("Sending payload: " + payload);
    
    int httpResponseCode = http.POST(payload); // Send POST request
    if (httpResponseCode > 0) {
      // If successful, display HTTP response
      String response = http.getString();
      Serial.println("Data sent successfully. HTTP Response: " + String(httpResponseCode));
      Serial.println("Server Response: " + response);
    } else {
      // If an error occurs, display the response code
      Serial.println("Error sending data. HTTP Response: " + String(httpResponseCode));
      Serial.println("Possible reasons: Invalid server URL or server is unreachable.");
    }
    http.end(); // End the HTTP request
  } else {
    // If WiFi is not connected, retry connecting
    Serial.println("WiFi not connected. Retrying...");
  }
}

