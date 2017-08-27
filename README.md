# KROL
Kid's Record Of Life - testing speech recognition voice assistant to keep track of your kid's poo, eat and sleep activities.

## Disclaimer
I'm a Python n00b, so if you have any suggestions on how to make it more pythonic, then please be my guest and add the issue or a pull request.

## Overview
This a test project to keep track of all the most important activities of your new born kid: when it ate, slept or made a poo. All of that with your voice, so you won't have to use your hands.
The spoken responses are in polish ;) but you should be able to translate the strings to your language.

Right now it just keeps track of the most recent of those activities.

## Requirements
1. Windows with SAPI5 for speaking (I think it's a standard feature in Win10)
1. Python3 with speech_recognition module (https://pypi.python.org/pypi/SpeechRecognition/) and PocketSphinx-Python
1. Wit.ai account (it's free)
1. Optional: there's a Visual Studio PTVS solution in src folder

## How to use it
Just run `main.py`:

```
python main.py
```

TODO

## Windows Audio Device Graph Isolation (audiodg.exe) issue
Sometimes, the audiodg.exe service might consume all of your RAM. This is probably casued by some bugs in either Windows 8/10 or audio drivers. In my case (Lenovo T540p), updating the Realtek audio drivers, motherboard drivers, disabling microphone enhancments and disabling microphone exclusive modes helped a lot and the memory consumption dropped significantly.
