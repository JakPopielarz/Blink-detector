#include "utils.h"
#include <math.h>
#include <iostream>

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


/////////////////////////////////////////////////////////////////////////////////
//                SIGNAL ANALYSIS FUNCTIONS
/////////////////////////////////////////////////////////////////////////////////

// Helper function to help compare two doubles with a given precision.
// It will not be exact in some cases due to floating point number
// representation, but eh - good enough for my purposes.
bool compare(double value1, double value2, int precision) {
    std::cout << "Value 1: " << value1 << "; Value 2: " << value2 << "\n"; 
    return std::abs(value1 - value2) < std::pow(10, -precision);
}

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
      sum += pow((array[i] - mean), 2);
   }
   return sqrt(sum / size);
}

/*
Calculate if single point is a peak:
Check if the point's value is inside the interval:
( mean - (std*stdMultiple); mean + (std*stdMultiple) )
If it is - check if the point's value is higher than mean
   If it is - it's a "top" peak - on plot would look like: /\
      Then return 1
   Else - it's a "bottop" peak - on plot would look like: \/
   The "Else" case doesn't interest us, so it has been ommited.
In all other cases return 0
*/
int checkDatum(int datum, double mean, double std, int stdMultiple) {
  if ((datum - mean) > (stdMultiple * std)) {
   // if point value exceeds the border value ("upwards")
      if (datum > mean) {
         return 1;
     }
   }
   return 0;
}

/*
Analyse raw detector values, WITHOUT pre-calculated mean and standard deviation
*/
void detect(int array[], int size, int thresholdValue, int signals[], int* newPointCount, int* lastFilledIndex) {
   double mean = calculateMean(array, size);
   double std = calculateStd(array, size, mean);

   detect(array, size, mean, std, thresholdValue, signals, newPointCount, lastFilledIndex);
}

/*
Analyse raw detector values, WITH pre-calculated mean and standard deviation
*/
void detect(int array[], int size, double mean, double std, int thresholdValue, int signals[], int* newPointCount, int* lastFilledIndex) {
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
