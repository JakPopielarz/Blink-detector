#include "utils.h"

#define VALUE_ARRAY_SIZE 10

// Pin / device variables
int sensorPin = A0;
int sensorValue = 0;
int ledPin = 3;

// Raw data array variables
int values[VALUE_ARRAY_SIZE]; 
int lastFilledValueIndex = -1;

// Signal analysis algorithm variables
double average = 0.0;
double baseThreshold = 10.0;
double threshold = 200.0;

// Analysis data array variables
int signals[VALUE_ARRAY_SIZE];
int numberOfNewPoints = 0;

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
   setupArray(values, VALUE_ARRAY_SIZE, -1);
   setupArray(signals, VALUE_ARRAY_SIZE, 0);

   Serial.begin(9600);
   pinMode(sensorPin, INPUT);
   // pinMode(ledPin, OUTPUT);
   analogReference(INTERNAL);
}
 
void loop(void) {
   // digitalWrite(ledPin, HIGH);
   delay(2);
   sensorValue = analogRead(sensorPin);
   Serial.print("Sensor value: ");
   Serial.println(sensorValue);
   
   appendToSizeLimited(values, VALUE_ARRAY_SIZE, &lastFilledValueIndex,sensorValue);
   numberOfNewPoints ++;

   // serialPrintArray(values, VALUE_ARRAY_SIZE);
   detect(values, VALUE_ARRAY_SIZE, threshold, signals, &numberOfNewPoints, &lastFilledValueIndex);
   
   Serial.print("Threshold: ");
   Serial.print(threshold);
   Serial.print(" || result ( ");
   Serial.print(lastFilledValueIndex);
   Serial.print(" ): ");
   Serial.println(signals[lastFilledValueIndex]);
   
   Serial.print("Signals: ");
   serialPrintArray(signals, VALUE_ARRAY_SIZE);

   delay(1000);
   // digitalWrite(ledPin, LOW);
   delay(7);
}
