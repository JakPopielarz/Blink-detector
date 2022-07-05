#include "catch.hpp"
#include "..\utils.h"

// CATCH2 DOCUMENTATION / TUTORIAL: https://github.com/catchorg/Catch2/blob/v2.x/docs/tutorial.md

TEST_CASE("Two doubles are compared with given precision", "[critical][compare]") {
    double a = 35.6242314312;
    double b = 35.6247636523;
    double c = 35.6242314312;
    REQUIRE(compare(a, b, 3));
    REQUIRE_FALSE(compare(a, b, 7));
    REQUIRE(compare(a, c, 10));
}

TEST_CASE("Mean of an array is calculated", "[mean]") {
    int array0[] = {0, 0, 0, 0, 0};
    REQUIRE(calculateMean(array0, 5) == 0);
    int array1[] = {-100, -40, 23, 1, -4};
    REQUIRE(calculateMean(array1, 5) == -24);
    int array2[] = {100, 40, 23, 1, -4, 1, 124, -123, 18};
    REQUIRE(calculateMean(array2, 9) == 20);
    int array3[] = {};
    REQUIRE(std::isnan(calculateMean(array3, 0)));
    int array4[] = {10};
    REQUIRE(calculateMean(array4, 1) == 10);
    int array5[] = {100, 40, 23, 1, 4};
    REQUIRE(compare(calculateMean(array5, 5), 33.6, 9));
}

TEST_CASE("Standard deviation of an array is calculated", "[std]") {
    int array0[] = {0, 0, 0, 0, 0};
    REQUIRE(compare(calculateStd(array0, 5, 0), 0, 3));
    int array1[] = {-100, -40, 23, 1, -4};
    REQUIRE(compare(calculateStd(array1, 5, -24), 43.0488, 3));
    int array2[] = {100, 40, 23, 1, -4, 1, 124, -123, 18};
    REQUIRE(compare(calculateStd(array2, 9, 20), 66.145, 3));
    int array3[] = {};
    REQUIRE(std::isnan(calculateStd(array3, 0, 0)));
    int array4[] = {10};
    REQUIRE(compare(calculateStd(array4, 1, 10), 0.0, 3));
    int array5[] = {100, 40, 23, 1, 4};
    REQUIRE(compare(calculateStd(array5, 5, 33.6), 36.059, 3));
}
