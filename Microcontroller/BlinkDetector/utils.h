#ifndef UTILS_H
#define UTILS_H

void setupArray(int array[], int size, int initValue);
void appendToSizeLimited(int array[], int size, int value, int* lastFilledIndex, bool incrementCount);
void serialPrintArray(int array[], int size);
bool compare(double value1, double value2, int precision);
double calculateMean(int array[], int size);
double calculateStd(int array[], int size, double mean);
int checkDatum(int datum, double mean, double std, double stdMultiple);
void detect(int array[], int size, double stdMultiple, int signals[], int* newPointCount, int* lastFilledIndex);
void detect(int array[], int size, double mean, double std, double stdMultiple, int signals[], int* newPointCount, int* lastFilledIndex);

#endif
