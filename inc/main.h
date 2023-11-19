/**
 * main.h
 * Copyright (c) AnoesisAudio 2023
 */

#ifndef MAIN_H
#define MAIN_H

#include <string>

std::string text {"This works"};
std::string getText();

struct MyStruct {
    int myNum = 0;
    std::string myString = "this is now working";

    std::string getMyString() {return myString;};
};

#endif //MAIN_H
