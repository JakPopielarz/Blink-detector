#include "catch.hpp"
#include "..\utils.h"

#include <iostream>

// CATCH2 DOCUMENTATION / TUTORIAL: https://github.com/catchorg/Catch2/blob/v2.x/docs/tutorial.md


TEST_CASE("Array is initialized with given values", "[setupArray]") {
    int array[20];
    int size = 20;
    
    SECTION("Initializing with -1") {
        int value = -1;

        setupArray(array, size, value);
        for (int i=0; i<size; i++) {
            REQUIRE(array[i] == value);
        }
    }
    
    SECTION("Initializing with 1") {
        int value = 1;

        setupArray(array, size, value);
        for (int i=0; i<size; i++) {
            REQUIRE(array[i] == value);
        }
    }
}

// void appendToSizeLimited(int array[], int size, int value, int* lastFilledIndex, bool incrementCount);

TEST_CASE("Value is added to the array", "[appendToSizeLimited]") {
    int array[10];
    int size = 10;
    int lastFilledIndex = -1;
    
    SECTION("Appending, with increment true") {
        for (int i=0; i<size; i++) {
            appendToSizeLimited(array, size, i, &lastFilledIndex, true);
        }

        appendToSizeLimited(array, size, size, &lastFilledIndex, true);

        for (int i=0; i<size; i++) {
            REQUIRE(array[i] == i+1);
        }
    }
    
    SECTION("Appending, with increment false") {
        // setting the array values to 0, to make sure there's no memory garbage in the way
        for (int i=0; i<size; i++) {
            array[i] = 0;
        }

        for (int i=0; i<size; i++) {
            appendToSizeLimited(array, size, i, &lastFilledIndex, false);
        }

        appendToSizeLimited(array, size, size+1, &lastFilledIndex, false);

        REQUIRE(array[0] == size+1);

        for (int i=1; i<size; i++) {
            REQUIRE(array[i] == 0);
        }
    }
}
