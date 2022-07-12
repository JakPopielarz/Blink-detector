#ifndef UTILS_H
#define UTILS_H

void setupArray(int array[], int size, int initValue);
void appendToSizeLimited(int array[], int size, int value, int* lastFilledIndex, bool incrementCount);
void serialPrintArray(int array[], int size);
bool compare(double value1, double value2, int precision);
double calculateMean(int array[], int size);
double calculateStandardDeviation(int array[], int size, double mean);
int checkDatum(int datum, double mean, double standardDeviation, double standardDeviationMultiple);
void detect(int array[], int size, double standardDeviationMultiple, int signals[], int* newPointCount, int* lastFilledIndex, bool incrementCount);
void detect(int array[], int size, double mean, double standardDeviation, double standardDeviationMultiple, int signals[], int* newPointCount, int* lastFilledIndex, bool incrementCount);

#endif
