#include "catch.hpp"
#include "..\utils.h"

// CATCH2 DOCUMENTATION / TUTORIAL: https://github.com/catchorg/Catch2/blob/v2.x/docs/tutorial.md

TEST_CASE("Data point is compared to given values: 100, 10, 35, 11, 24, 3, 34, 11, 23, 12, 31", "[checkDatum]") {
    int array[] = {100, 10, 35, 11, 24, 3, 34, 11, 23, 12, 31};
    int arraySize = 11;
    // using functions from utils, because they are tested in other file
    double mean = calculateMean(array, arraySize);
    double standardDeviation = calculateStandardDeviation(array, arraySize, mean);

    // making sure the values are correct
    REQUIRE(compare(mean, 26.727, 3));
    REQUIRE(compare(standardDeviation, 25.377, 3));

    double standardDeviationMultiple = 2;

    SECTION("Checking 100 returns 1") {
        REQUIRE(checkDatum(array[0], mean, standardDeviation, standardDeviationMultiple) == 1);
    }

    SECTION("Checking other values returns 0") {
        for (int i=1; i<arraySize; i++) {
            REQUIRE(checkDatum(array[i], mean, standardDeviation, standardDeviationMultiple) == 0);
        }
    }
}

TEST_CASE("Array is properly analyzed (without precalculated mean and standard deviation)\nArray [100, 10, 35, 11, 24, 3, 34, 11, 23, 12, 31] results with [1, 0 ... 0]\n", "[detect][with calculating]") {
    int array[] = {100, 10, 35, 11, 24, 3, 34, 11, 23, 12, 31};
    int arraySize = 11;
    int newPoints = 11;
    int lastFilledIndex = -1;

    double standardDeviationMultiple = 2;

    DataContainer signals = DataContainer(-1);;
    DataContainer data = DataContainer(0);

    int j = 1;
    for (int i=0; i<data.getMaxLimit(); i++) {
        if (j >= arraySize)
            j = 1;

        if (i < arraySize) {
            data.data[i] = array[i];
        } else {
            data.data[i] = array[j];
            j ++;
        }
    }

    // passing true as the last argument, because otherwise lastFilledIndex will not be incremented - all values saved
    // in the same place in the signals array
    detect(&data, standardDeviationMultiple, &signals);

    SECTION("First detection result is 1") {
        REQUIRE(signals.data[0] == 1);
    }

    SECTION("Other detection results are 0") {
        for (int i=1; i<signals.getMaxLimit(); i++) {
            REQUIRE(signals.data[i] == 0);
        }
    }
}

TEST_CASE("Array is properly analyzed (with precalculated mean and standard deviation)Array [100, 10, 35, 11, 24, 3, 34, 11, 23, 12, 31] results with [1, 0 ... 0]\n", "[detect][precalculated]") {
    int array[] = {100, 10, 35, 11, 24, 3, 34, 11, 23, 12, 31};
    int arraySize = 11;

    double standardDeviationMultiple = 2;

    DataContainer signals = DataContainer(-1);;
    DataContainer data = DataContainer(0);

    int j = 1;
    for (int i=0; i<data.getMaxLimit(); i++) {
        if (j >= arraySize)
            j = 1;

        if (i < arraySize) {
            data.data[i] = array[i];
        } else {
            data.data[i] = array[j];
            j ++;
        }
    }

    // using functions from utils, because they are tested in other file
    double mean = calculateMean(data.data, arraySize);
    double standardDeviation = calculateStandardDeviation(data.data, arraySize, mean);

    // making sure the values are correct
    REQUIRE(compare(mean, 26.727, 3));
    REQUIRE(compare(standardDeviation, 25.377, 3));

    // passing true as the last argument, because otherwise lastFilledIndex will not be incremented - all values saved
    // in the same place in the signals array
    detect(&data, mean, standardDeviation, standardDeviationMultiple, &signals);

    SECTION("First detection result is 1") {
        REQUIRE(checkDatum(data.data[0], mean, standardDeviation, standardDeviationMultiple) == 1);
        REQUIRE(signals.data[0] == 1);
    }

    SECTION("Other detection results are 0") {
        for (int i=1; i<signals.getMaxLimit(); i++) {
            REQUIRE(signals.data[i] == 0);
        }
    }
}
