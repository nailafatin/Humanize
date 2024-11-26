# Overview

This tool generates speech from text using Microsoft's edge-tts service and plays the audio via pygame. It offers customizable pitch, rate, and voice selection, along with the option to save audio as a WAV file.

# Features

## Text-to-Speech Conversion  
Converts input text into natural-sounding speech.  

1. **Voice Customization**: Adjust pitch, rate, and voice type.  
2. **Audio Playback**: Play generated speech directly.  
3. **Save Audio**: Download generated audio as a WAV file.  

# Requirements  

## Python Libraries  

Install required libraries with:  
```bash
pip install -r requirements.txt

#Required Libraries:

.edge-tts
.pygame
.tkinter (usually pre-installed)
.asyncio

OS-Specific Prerequisites

#For Linux (Ubuntu, Parrot OS, etc.):

#Install Python 3 and pip:

    sudo apt update && sudo apt install python3 python3-pip

#Install virtualenv:

    pip3 install virtualenv

#Create and activate a virtual environment:

     python3 -m venv venv  
     source venv/bin/activate

#Install dependencies in the virtual environment:

    pip install -r requirements.txt

#For Windows:

    Install Python 3, ensuring pip is added to PATH during installation.
    Install virtualenv:

    pip install virtualenv

#Create and activate a virtual environment:

    python -m venv venv  
    .\venv\Scripts\activate

Install dependencies in the virtual environment:

    pip install -r requirements.txt

#For macOS:

#Install Python 3 via Homebrew:

    brew install python

#Install virtualenv:

    pip3 install virtualenv

#Create and activate a virtual environment:

#virtualenv venv  
source venv/bin/activate

#Install dependencies:

    pip install -r requirements.txt

Usage

    Run the script : python3 tts.py

1.Input text via the GUI or terminal.
2.Customize pitch, rate, or voice settings.
3.Play the speech or download it as a WAV file.
