#!/bin/bash

pip install -r requirements.txt
sudo apt-get update
sudo apt-get install libssl1.0.0 libasound2
pip install azure-cognitiveservices-speech