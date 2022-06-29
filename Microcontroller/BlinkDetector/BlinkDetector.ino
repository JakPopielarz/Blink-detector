#include <math.h>

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

/////////////////////////////////////////////////////////////////////////////////
//                ARRAY FUNCTIONS
/////////////////////////////////////////////////////////////////////////////////

/*
Setup array of values - set every element to a given value,
which indicates it hasn't been used yet.
*/
void setupArray(int array[], int size, int initValue) {
   for (int i=0; i<size; i++) {
      array[i] = initValue;
   }
}

/*
Save a value to the array - if there are still elements previously not used
override them; if the array is already full - shift elements to the left and
insert new one on the end.
*/
void appendToSizeLimited(int array[], int size, int value, int* lastFilledIndex, bool incrementCount=true) {
   if (*lastFilledIndex < size-1) {
      int index = *lastFilledIndex + 1;
      array[index] = value;
      if (incrementCount)
         *lastFilledIndex = *lastFilledIndex + 1;
   } else {
      for (int i=0; i<size-1; i++) {
         array[i] = array[i+1];
      }
      array[size-1] = value;
   }
}

/*
Print out an array in one line:
[x0, x1, x2, x3, x4, ]
*/
void serialPrintArray(int array[], int size) {
   Serial.print("[");
   for (int i=0; i<size; i++) {
      Serial.print(array[i]);
      Serial.print(", ");
   }
   Serial.println("]");
}

/////////////////////////////////////////////////////////////////////////////////
//                SIGNAL ANALYSIS FUNCTIONS
/////////////////////////////////////////////////////////////////////////////////

/*
Calculate mean (average) of int array
*/
double calculateMean(int array[], int size) {
   double sum = 0.0;

   for (int i=0; i<size; i++) {
      sum += array[i];
   }
   return sum / size;
}

/*
Calculate standard deviation of int array
*/
double calculateStd(int array[], int size, double mean) {
   double sum = 0.0;

   for (int i=0; i<size; i++) {
      sum += square(array[i] - mean);
   }

   return sum / size;
}

/*
Calculate if single point is a peak
*/
bool checkDatum(int datum, double mean, double std, int thresholdValue) {
//   if (abs(datum - mean) > (thresholdValue * std)) {
  if (datum > thresholdValue) {
   // if point value exceeds the border value ("upwards")
      // if (datum > mean) {
         return true;
   //   }
   } else {
      return false;
   }
}

/*
Analyse raw detector values, WITHOUT pre-calculated mean and standard deviation
*/
void detect(int array[], int size, int thresholdValue, int* newPointCount, int* lastFilledIndex) {
   double mean = calculateMean(array, size);
   double std = calculateStd(array, size, mean);

   detect(array, size, mean, std, thresholdValue, newPointCount, lastFilledIndex);
}

/*
Analyse raw detector values, WITH pre-calculated mean and standard deviation
*/
void detect(int array[], int size, double mean, double std, int thresholdValue, int* newPointCount, int* lastFilledIndex) {
    // threshold = baseThreshold * std + mean; // TODO: CHECK IF THRESHOLD CALCULATION WORKS - something's not right, standard deviation / mean calculation?
   // there's no need to iterate through the whole data point array - the old points have been checked already
   // therefore iterate only through the part with new points (added since last analysis)
   for (int i=size-*newPointCount; i<size; i++) {
      int result = checkDatum(array[i], mean, std, thresholdValue);
      appendToSizeLimited(signals, size, result, lastFilledIndex, false);
   }
   // checked all new points, so clear the counter
   *newPointCount = 0;
}



/////////////////////////////////////////////////////////////////////////////////
//                CONTROL FUNCTIONS
/////////////////////////////////////////////////////////////////////////////////

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
   detect(values, VALUE_ARRAY_SIZE, threshold, &numberOfNewPoints, &lastFilledValueIndex);
   
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
