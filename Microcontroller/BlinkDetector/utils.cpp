#include "utils.h"
#include <math.h>
//#include <iostream>

DataContainer::DataContainer(int initValue) {
    for (int i=0; i<maxLimit; i++) {
        data[i] = initValue;
    }
}

void DataContainer::appendToData(int value) {
    if (lastFilledIndex < maxLimit-1) {
        int index = lastFilledIndex + 1;
        data[index] = value;
        if (incrementCount)
            lastFilledIndex++;
    } else {
        for (int i=0; i<maxLimit-1; i++) {
            data[i] = data[i+1];
        }
        data[maxLimit-1] = value;
    }
}


/////////////////////////////////////////////////////////////////////////////////
//                SIGNAL ANALYSIS FUNCTIONS
/////////////////////////////////////////////////////////////////////////////////

// Helper function to help compare two doubles with a given precision.
// It will not be exact in some cases due to floating point number
// representation, but eh - good enough for my purposes.
bool compare(double value1, double value2, int precision) {
    // std::cout << "Value 1: " << value1 << "; Value 2: " << value2 << "\n"; 
    return fabs(value1 - value2) < pow(10, -precision);
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
double calculateStandardDeviation(int array[], int size, double mean) {
    double sum = 0.0;

    for (int i=0; i<size; i++) {
        sum += pow((array[i] - mean), 2);
    }
    return sqrt(sum / size);
}

/*
Calculate if single point is a peak:
Check if the point's value is inside the interval:
( mean - (standardDeviation*standardDeviationMultiple); mean + (standardDeviation*standardDeviationMultiple) )

On a plot that interval would look like a "band".

If the value is outside of the band - check if the point's value is higher than mean
   If it is - it's outside the "top" of the band
      Then return 1
   Else - it's outside the "bottom" of the band
   The "Else" case doesn't interest us, so it has been ommited.
In all other cases return 0
*/
int checkDatum(int datum, double mean, double standardDeviation, double standardDeviationMultiple) {
    if ((datum - mean) > (standardDeviationMultiple * standardDeviation)) {
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
void detect(DataContainer* data, double standardDeviationMultiple, DataContainer* signals) {
    double mean = calculateMean(data->data, data->getMaxLimit());
    double standardDeviation = calculateStandardDeviation(data->data, data->getMaxLimit(), mean);

    detect(data, mean, standardDeviation, standardDeviationMultiple, signals);
}

/*
Analyse raw detector values, WITH pre-calculated mean and standard deviation
*/
void detect(DataContainer* data, double mean, double standardDeviation, double standardDeviationMultiple, DataContainer* signals) {
    // there's no need to iterate through the whole data point array - the old points have been checked already
    // therefore iterate only through the part with new points (added since last analysis).
    // for now and for simplicity - iterating through all points
    int size = data->getMaxLimit();
    for (int i=0; i<size; i++) {
        int result = checkDatum(data->data[i], mean, standardDeviation, standardDeviationMultiple);
        signals->appendToData(result);
    }
}
