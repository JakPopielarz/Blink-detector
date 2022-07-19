#ifndef UTILS_H
#define UTILS_H

class DataContainer {
    private:
        enum { maxLimit = 50 };

        int lastFilledIndex = -1;
        bool incrementCount = true;
        int newElementCount = 0;
    public:
        int data[maxLimit];
        DataContainer(int initValue);

        void appendToData(int value);

        void setIncrementFlag(bool value) { incrementCount = value; }
        bool getIncrementFlag() { return incrementCount; }

        void setLastFilledIndex(int value) { lastFilledIndex = value; }
        int getLastFilledIndex() { return lastFilledIndex; }

        int getMaxLimit() { return maxLimit; }
        
        void setNewElementCount(int value) { newElementCount = value; }
        bool getNewElementCount() { return newElementCount; }
        void incrementNewElementCount() { newElementCount++; }
};

bool compare(double value1, double value2, int precision);
double calculateMean(int array[], int size);
double calculateStandardDeviation(int array[], int size, double mean);
int checkDatum(int datum, double mean, double standardDeviation, double standardDeviationMultiple);
void detect(DataContainer* data, double standardDeviationMultiple, DataContainer* signals) 
void detect(DataContainer* data, double mean, double standardDeviation, double standardDeviationMultiple, DataContainer* signals);

#endif
