# Notes for Python use in anolib

## Purpose

This folder contains tests, experiments, and the resulting designs that are implemented by anolib. The pytest library is used to enable TDD.

Tests are simply run with the word 'pytest' like:

```zsh
cd anolib
pytest
```

## Structure

This project contains the following folders.

_Note_: The "main" application (made up for main.h and main.cpp) is only used for testing the application, for now. This may continue to exist, or it may be deleted in the future.

- __inc__ holds include files for all classes; these are in sub-folders for each topical area e.g., filters, oscillators.
- __libs__ holds libraries used.
- __python__ holds files used for algorithm design (including those aimed at TDD, which are prefixed with _test__ to enable pytest).
- __src__ holds compilation units defined in __inc__; the folder structure should match.
- __tests__ holds testing files used to test the classes defined in __inc__ and __src__.
