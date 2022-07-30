#include "catch.hpp"
#include "..\utils.h"

#include <iostream>

// CATCH2 DOCUMENTATION / TUTORIAL: https://github.com/catchorg/Catch2/blob/v2.x/docs/tutorial.md


TEST_CASE("Array is initialized with given values", "[DataContainer]") {

    SECTION("Initializing with -1") {
        int value = -1;

        DataContainer container(value);
        for (int i=0; i<container.getMaxLimit(); i++) {
            REQUIRE(container.data[i] == value);
        }
    }
    
    SECTION("Initializing with 1") {
        int value = 1;

        DataContainer container(value);
        for (int i=0; i<container.getMaxLimit(); i++) {
            REQUIRE(container.data[i] == value);
        }
    }
}


TEST_CASE("Value is added to the array", "[appendToData]") {
    
    SECTION("Appending, with increment true") {
        DataContainer container(0);

        for (int i=0; i<container.getMaxLimit(); i++) {
            container.appendToData(i);
        }

        container.appendToData(container.getMaxLimit());

        for (int i=0; i<container.getMaxLimit(); i++) {
            REQUIRE(container.data[i] == i+1);
        }
    }
    
    SECTION("Appending, with increment false") {
        DataContainer container(0);
        container.setIncrementFlag(false);

        for (int i=0; i<container.getMaxLimit(); i++) {
            container.appendToData(i);
        }

        container.appendToData(container.getMaxLimit()+1);

        REQUIRE(container.data[0] == container.getMaxLimit()+1);

        for (int i=1; i<container.getMaxLimit(); i++) {
            REQUIRE(container.data[i] == 0);
        }
    }
}
