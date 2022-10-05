#include "NetworkUtils.h"

#include <EEPROM.h>

// File system
LittleFSConfig fileSystemConfig = LittleFSConfig();
static bool fsOK;

ESP8266WebServer server(80);    // Create a webserver object that listens for HTTP request on port 80

IPAddress softApIp(192, 168, 1, 1); // Create IP addresses for the soft AP
IPAddress softApGateway(192, 168, 1, 1);
IPAddress softApSubnet(255, 255, 255, 0);

int togglePin = D1;
bool serverRunning = false;

String keyOrMouse;
String bind;

StoredSettings romSettings;

// Setup functions

void setupFS() {
  fileSystemConfig.setAutoFormat(false);    // configure the file system - make sure it won't be formatted automatically
  LittleFS.setConfig(fileSystemConfig);

  fsOK = LittleFS.begin();
  Serial.println(fsOK ? "Filesystem initialized. Files:" : "Filesystem init failed!");

  if (fsOK) { // if the file system started properly
    Dir dir = LittleFS.openDir("/"); // iterate over files saved and print out their names
    while (dir.next()) {
      Serial.println(dir.fileName());
    }
    Serial.println();
  }
}

void setupServer() {
  server.on("/", handleRoot);               // Call the 'handleRoot' function when a client requests URI "/"
  server.on("/index.js", handleJs);
  server.on("/bootstrap.min.css", handleBootstrap);
  server.onNotFound(handleNotFound);        // When a client requests an unknown URI (i.e. something other than "/"), call function "handleNotFound"
}

void setupNetworkUtils() {
  Serial.println("\n");
  pinMode(togglePin, INPUT_PULLUP); // configure toggle switch pin
  pinMode(LED_BUILTIN, OUTPUT); // configure on-board LED pin
  digitalWrite(LED_BUILTIN, HIGH);

  romSettings = getStoredSettings();
  keyOrMouse = romSettings.keyMouse;
  bind = romSettings.bind;
  Serial.println("Read from EEPROM: Keyboard/mouse: " + keyOrMouse + "; Bind: " + bind + "\n");

  setupFS();
  setupServer();
}

void loopNetworkUtils(void) {
  if (digitalRead(togglePin) == 1 && !serverRunning) { // if server's not running and the config toggle is on
    startServer();
  } else if (digitalRead(togglePin) == 0 && serverRunning) { // if server's running and the config toggle is off
    stopServer();
  }

  if (serverRunning) {
    server.handleClient();                    // Listen for HTTP requests from clients
  }
}


// HTML handlers implementations

void handleRoot() {                         // Read the page files from file system and stream it to the client
  if (server.arg("keyboard-mouse") != "")
    keyOrMouse = server.arg("keyboard-mouse");
  if (server.arg("keybind") != "")
    bind = server.arg("keybind");
  saveSettings(keyOrMouse, bind);

  streamFile("index.html", "text/html");
}

void handleJs() {
  streamFile("index.js", "text/javascript");
}

void handleBootstrap() {
  streamFile("bootstrap.min.css", "text/css");
}

void handleNotFound() {
  server.send(404, "text/plain", "404: Not found\r\n"); // Send HTTP status 404 (Not Found) when there's no handler for the URI in the request
}

void streamFile(String path, String contentType) {
  if (!fsOK) {                              // If file system is not initialized properly
    replyServerError("File system initialization error"); // reply to the client with an error
    return;
  }

  if (LittleFS.exists(path)) {              // Make sure the file is there
    File file = LittleFS.open(path, "r");   // read the file
    if (server.streamFile(file, contentType) != file.size()) {
      Serial.println("Sent less data than expected!");  // stream it's contents to the client and make sure it's all streamed
    }
    file.close();                           // close the file
  } else {
    replyServerError("Lost page file: " + path);
  }
}

void replyServerError(String msg) {
  Serial.println(msg);
  server.send(500, "text/plain", msg + "\r\n");
}


// Server handling utilities

void startServer() {
  WiFi.softAPConfig(softApIp, softApGateway, softApSubnet);
  WiFi.softAP("Blink");

  server.begin();                           // Actually start the server
  Serial.println("HTTP server started");
  serverRunning = true;
  delay(150);
  digitalWrite(LED_BUILTIN, LOW); // light up on-board LED
}

void stopServer() {
  WiFi.softAPdisconnect(true);
  server.close();
  server.stop();
  Serial.println("HTTP server stopped");
  serverRunning = false;
  digitalWrite(LED_BUILTIN, HIGH); // turn off on-board LED
}


// Saving / reading config from on-board memory utilities

void saveSettings(String keyMouse, String bind) {
  uint addr = 0;

  strcpy(romSettings.keyMouse, keyMouse.c_str());
  strcpy(romSettings.bind, bind.c_str());

  EEPROM.begin( 512 );
  EEPROM.put(addr, romSettings);
  EEPROM.end();
}

StoredSettings getStoredSettings() {
  uint addr = 0;
  EEPROM.begin(512);
  EEPROM.get(addr, romSettings);
  EEPROM.end();
  return romSettings;
}

void wipeSettings() {
  struct StoredSettings {
    char keyMouse[128];
    char bind[128];
  } clearSettings;

  strcpy(clearSettings.keyMouse, "key");
  strcpy(clearSettings.bind, "enter");

  uint addr = 0;
  EEPROM.begin( 512 );
  EEPROM.put(addr, clearSettings);
  EEPROM.end();
}
