#include <catch2/catch_all.hpp>

#include "../inc/main.h"

MyStruct testStructure;

TEST_CASE("are tests are working", "[test 1]")
{
    REQUIRE(1 == 1);
    REQUIRE(2 == 2);
    REQUIRE(3 == 3);
}

TEST_CASE("are classes being created", "[test 2]")
{
    REQUIRE(testStructure.getMyString() == "this is now working");
}
