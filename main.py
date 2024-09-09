import speech_recognition as sr
import pyttsx3 as tts

# Include module imports here
from Modules.Spotify import Spotify
from Modules.Weather import Weather
from Modules.Sports import Sports
from Envs import *
from AudioDriver import AudioDriver
env = Env()
d = AudioDriver()

# Initiate modules. Note that overlaps will be handled by priority in this list
modules = [Spotify(), Weather(), Sports(env), Followup(d)]
triggers = {}
for m in modules:
    for t in m.triggers:
        if t not in triggers.keys():
            triggers[t] = m

# Main commands


def FindModule(text):
    for tr, mo in triggers.items():
        if tr in text:
            print("Identified module: ", mo.name)
            return mo.process(text)
    return "Couldn't locate module, trying again", None


# Add more wake words
WAKE = "hey luna"
while True:
    print("Listening")
    command = d.Listen()
    if command.count(WAKE) > 0:
        print("Awaiting Command")
        command2 = d.Listen()

        if command2:
            response, callback = FindModule(command2)
            if response:
                d.Say(response)
            if callback:
                callback()
