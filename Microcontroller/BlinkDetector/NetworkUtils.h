#ifndef NETWORK_UTILS_H
#define NETWORK_UTILS_H

#include <ESP8266WebServer.h>
#include <LittleFS.h>
#include <Arduino.h>

// Values saved to EEPROM for persistent storage of settings
struct StoredSettings {
  char keyMouse[128];
  char bind[128];
};

void handleRoot();              // function prototypes for HTTP handlers
void handleJs();
void handleBootstrap();
void handleNotFound();
void streamFile(String path, String contentType);
void replyServerError(String msg);
void startServer();             // function prototypes for server handling utilities
void stopServer();
void saveSettings(String keyMouse, String bind);  // function prototypes for handling stored settings
StoredSettings getStoredSettings();
void wipeSettings();
void setupFS();                 // function prototypes for setup handlers
void setupServer();
void setupNetworkUtils();
void loopNetworkUtils();        // function prototype for run handler

#endif
