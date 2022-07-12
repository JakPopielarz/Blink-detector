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

    int signals[11] = {-1};

    // passing true as the last argument, because otherwise lastFilledIndex will not be incremented - all values saved
    // in the same place in the signals array
    detect(array, arraySize, standardDeviationMultiple, signals, &newPoints, &lastFilledIndex, true);

    SECTION("First detection result is 1") {
        REQUIRE(signals[0] == 1);
    }

    SECTION("Other detection results are 0") {
        for (int i=1; i<arraySize; i++) {
            REQUIRE(signals[i] == 0);
        }
    }
}

TEST_CASE("Array is properly analyzed (with precalculated mean and standard deviation)Array [100, 10, 35, 11, 24, 3, 34, 11, 23, 12, 31] results with [1, 0 ... 0]\n", "[detect][precalculated]") {
    int array[] = {100, 10, 35, 11, 24, 3, 34, 11, 23, 12, 31};
    int arraySize = 11;
    int newPoints = 11;
    int lastFilledIndex = -1;

    // using functions from utils, because they are tested in other file
    double mean = calculateMean(array, arraySize);
    double standardDeviation = calculateStandardDeviation(array, arraySize, mean);

    // making sure the values are correct
    REQUIRE(compare(mean, 26.727, 3));
    REQUIRE(compare(standardDeviation, 25.377, 3));

    double standardDeviationMultiple = 2;

    int signals[11] = {-1};

    // passing true as the last argument, because otherwise lastFilledIndex will not be incremented - all values saved
    // in the same place in the signals array
    detect(array, arraySize, mean, standardDeviation, standardDeviationMultiple, signals, &newPoints, &lastFilledIndex, true);

    SECTION("First detection result is 1") {
        REQUIRE(checkDatum(array[0], mean, standardDeviation, standardDeviationMultiple) == 1);
        REQUIRE(signals[0] == 1);
    }

    SECTION("Other detection results are 0") {
        for (int i=1; i<arraySize; i++) {
            REQUIRE(signals[i] == 0);
        }
    }
}
