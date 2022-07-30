#include "utils.h"

// Pin / device variables
int sensorPin = A0;
int sensorValue = 0;

int ledPin = 3;

// Signal analysis algorithm variables
double standardDeviationMultiple = 2.0;

// Analysis data containers variables
DataContainer rawData = DataContainer(0);
DataContainer processingResults = DataContainer(-1);

/*
Print out an array in one line:
[x0, x1, x2, x3, x4, ]

Using Arduino-Specific includes / methods, therefore defined in the .ino file
*/
void serialPrintArray(int array[], int size) {
   Serial.print("[");
   for (int i=0; i<size; i++) {
      Serial.print(array[i]);
      Serial.print(", ");
   }
   Serial.println("]");
}


void setup(void) {
   Serial.begin(9600);
   pinMode(sensorPin, INPUT);
   // pinMode(ledPin, OUTPUT);
   analogReference(INTERNAL);
}
 
void loop(void) {
   // digitalWrite(ledPin, HIGH);
   delay(2);
   sensorValue = analogRead(sensorPin);
   rawData.appendToData(sensorValue);
   detect(&rawData, standardDeviationMultiple, &processingResults);

   // output last detection result to the serial port
   Serial.println(processingResults.data[processingResults.getMaxLimit()-1]);
   
   delay(1000); // Delay 1s to allow easier debug
   delay(7);
}
