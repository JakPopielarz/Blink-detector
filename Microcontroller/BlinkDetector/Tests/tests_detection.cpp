#include "catch.hpp"
#include "..\utils.h"

// CATCH2 DOCUMENTATION / TUTORIAL: https://github.com/catchorg/Catch2/blob/v2.x/docs/tutorial.md

TEST_CASE("Data point is compared to given values: 100, 10, 35, 11, 24, 3, 34, 11, 23, 12, 31", "[checkDatum]") {
    int array[] = {100, 10, 35, 11, 24, 3, 34, 11, 23, 12, 31};
    int arraySize = 11;
    // using functions from utils, because they are tested in other file
    double mean = calculateMean(array, arraySize);
    double std = calculateStd(array, arraySize, mean);

    // making sure the values are correct
    REQUIRE(compare(mean, 26.727, 3));
    REQUIRE(compare(std, 25.377, 3));

    double valueStdMultiple = 2;

    SECTION("Checking 100 returns 1") {
        REQUIRE(checkDatum(array[0], mean, std, valueStdMultiple) == 1);
    }

    SECTION("Checking other values returns 0") {
        for (int i=1; i<arraySize; i++) {
            REQUIRE(checkDatum(array[i], mean, std, valueStdMultiple) == 0);
        }
    }
}
