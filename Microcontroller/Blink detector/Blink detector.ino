#include <math.h>

#define VALUE_ARRAY_SIZE 100

// Pin / device variables
int sensorPin = A0;
int sensorValue = 0;
int ledPin = 3;

// Raw data array variables
int values[VALUE_ARRAY_SIZE]; 
int lastFilledValueIndex = -1;

// Signal analysis algorithm variables
double average = 0.0;
double threshold = 10.0;
double mean_avg_filter = 0.0;
double mean_std_filter = 0.0;

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
void setupArray(int array[], int initValue) {
   for (int i=0; i<VALUE_ARRAY_SIZE; i++) {
      array[i] = initValue;
   }
}

/*
Save a value to the array - if there are still elements previously not used
override them; if the array is already full - shift elements to the left and
insert new one on the end.
*/
void appendToSizeLimited(int array[], int size, int value, bool incrementCount=true) {
   if (lastFilledValueIndex < size-1) {
      int index = lastFilledValueIndex + 1;
      array[index] = value;
      if (incrementCount)
         lastFilledValueIndex++;
   } else {
      for (int i=0; i<size-1; i++) {
         array[i] = array[i+1];
      }
      array[size-1] = value;
   }
}

/*
Save a raw detector value to the array - taking care of size limitations
*/
void saveValue(int valueArray[], int value) {
   appendToSizeLimited(valueArray, VALUE_ARRAY_SIZE, value);
   numberOfNewPoints ++;
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
bool checkDatum(int datum, double mean, double std) {
   if (abs(datum - mean) > (threshold * std)) {
   // if point value exceeds the border value ("upwards")
      if (datum > mean) {
         return 1;
      }
   } else {
      return 0;
   }
}

/*
Analyse raw detector values, WITHOUT pre-calculated mean and standard deviation
*/
void detect(int array[], int size) {
   double mean = calculateMean(array, size);
   double std = calculateStd(array, size, mean);

   detect(array, size, mean, std);
}

/*
Analyse raw detector values, WITH pre-calculated mean and standard deviation
*/
void detect(int array[], int size, double mean, double std) {
   threshold = threshold * std + mean; // TODO: CHECK IF THRESHOLD CALCULATION WORKS
   // there's no need to iterate through the whole data point array - the old points have been checked already
   // therefore iterate only through the part with new points (added since last analysis)
   for (int i=size-numberOfNewPoints; i<size; i++) {
      int = result = checkDatum(array[i], mean, std);
      appendToSizeLimited(signals, VALUE_ARRAY_SIZE, result, false);
   }
   // checked all new points, so clear the counter
   numberOfNewPoints = 0;
}



/////////////////////////////////////////////////////////////////////////////////
//                CONTROL FUNCTIONS
/////////////////////////////////////////////////////////////////////////////////

void setup(void) {
   setupArray(values, -1);
   setupArray(signals, 0);

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
   
   saveValue(values, sensorValue);
   // serialPrintArray(values, VALUE_ARRAY_SIZE);
   detect(values, VALUE_ARRAY_SIZE);
   Serial.print("Threshold: ");
   Serial.print(threshold);
   Serial.print(" || result: ");
   Serial.println(signals[lastFilledValueIndex]);
   
   Serial.print("Signals: ");
   serialPrintArray(signals, VALUE_ARRAY_SIZE);

   delay(1);
   // digitalWrite(ledPin, LOW);
   delay(7);
}
