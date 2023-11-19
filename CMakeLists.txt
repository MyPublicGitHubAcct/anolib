cmake_minimum_required(VERSION 3.26)

set(BASENAME anolib)
project(BASENAME VERSION 0.01)

add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/libs/Catch2)

set(CMAKE_CXX_STANDARD 20)
add_executable("${BASENAME}" src/main.cpp)

##########################################

enable_testing() # need to create CTestTestfile.cmake files for each project

set(TESTFILES
        tests/TestTests.cpp
)

add_executable("${BASENAME}_tests" ${TESTFILES})

target_link_libraries("${BASENAME}_tests"
        PRIVATE
        Catch2::Catch2WithMain
)

target_include_directories("${BASENAME}_tests"
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)

include(${Catch2_SOURCE_DIR}/extras/Catch.cmake)
catch_discover_tests("${BASENAME}_tests")
