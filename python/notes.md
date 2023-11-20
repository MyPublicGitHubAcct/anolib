# Notes for Python use in anolib

## Purpose

This folder contains tests, experiments, and the resulting designs that are implemented by anolib. The pytest library is used to enable TDD.

Tests are simply run with the word 'pytest' like:

```zsh
cd anolib
pytest
```

## Structure

The files in this project are organized as described below. C and C++ code is in folders & Python uses a similar file naming convention.

- __inc__ holds include files for all classes; these are in sub-folders for each topical area e.g., filters, oscillators.
- __libs__ holds libraries used.
- __python__ holds files used for algorithm design. More on this below.
- __src__ holds compilation units defined in __inc__; the folder structure should match.
- __tests__ holds testing files used to test the classes defined in __inc__ and __src__.

__Note__: _The "main" application (made up for main.h and main.cpp) is only used for testing the application, for now. This may continue to exist, or it may be deleted in the future._

### Python files

- __z_sketch.py__ is used for experiments/design. The results of those experiments are copied into the associated __algo__ and __test__ files.

Four-character prefixes are used to describe purpose for each file. These are:
- _test_ includes scripts used to do testing of the algorithms defined in other files.
- _algo_ includes scripts used to perform something; these scripts are used by _test_ scripts.
- _hope_ includes data to be used as expectations for testing.
- _util_ includes scripts used for testing the algorithms, for example test waveforms.
- _ntbk_ files are Python notebooks used where they provide benefit beyond what is possible without them.

After the prefixes described above, a second set of characters are used to describe the purpose of the file.
- _audio_ for audio-specific classes.
- _core_ for core classes like containers, memory management, etc.
- _crypto_ for crypto.
- _dsp_ for dsp.
- _event_ for event processing.
- _midi_ for midi classes.
- _ui_ for user interface classes.
- _other_ for classes that don't fit in another category


### Juce library structure

To provide a means for being consistent with the industry, the JUCE library structure is used as a guide for organizing anolib. The JUCE library is organized like:

- audio_basics = Classes for audio buffer manipulation, midi message handling, synthesis, etc.
- audio_devices = Classes to play and record from audio and MIDI I/O devices
- audio_formats = Classes for reading and writing various audio file formats.
- audio_processors = Classes for loading and playing VST, AU, LADSPA, or internally-generated audio processors.
- audio_utils = Classes for audio-related GUI and miscellaneous tasks.
- core = The essential set of basic JUCE classes, as required by all the other JUCE modules. Includes text, container, memory, threading and i/o functionality.
- cryptography = Classes for various basic cryptography functions, including RSA, Blowfish, MD5, SHA, etc.
- data_structures = Classes for undo/redo management, and smart data structures.
- dsp = Classes for audio buffer manipulation, digital audio processing, filtering, oversampling, fast math functions etc.
- events = Classes for running an application's main event loop and sending/receiving messages, timers, etc.
- graphics = Classes for 2D vector graphics, image loading/saving, font handling, etc.
- gui_basics = Basic user-interface components and related classes.
- gui_extra = Miscellaneous GUI classes for specialised tasks.
- midi_ci = Classes facilitating communication via MIDI Capability Inquiry
- osc = Open Sound Control implementation.
