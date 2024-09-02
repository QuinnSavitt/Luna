import speech_recognition as sr
import pyttsx3 as tts

# Include module imports here
from Spotify import Spotify
from Weather import Weather
from Sports import Sports
from Envs import *
env = Env()

# Initiate modules. Note that overlaps will be handled by priority in this list
modules = [Spotify(), Weather(), Sports(env)]
triggers = {}
for m in modules:
    for t in m.triggers:
        if t not in triggers.keys():
            triggers[t] = m
print(triggers)
r = sr.Recognizer()
mic = sr.Microphone()

# Main commands

def Listen() -> str:
    with mic as source:
        r.adjust_for_ambient_noise(source, 0.1)
        audio = r.listen(source, timeout=5, phrase_time_limit=4)
        command = ""

        try:
            command = r.recognize_google(audio)
            print(command)
        except Exception as e:
            print("Exception: " + str(e))

        return command.lower()


def Say(text: str):
    engine = tts.init()
    engine.say(text)
    engine.runAndWait()


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
    command = Listen()
    if command.count(WAKE) > 0:
        print("Awaiting Command")
        command2 = Listen()

        if command2:
            response, callback = FindModule(command2)
            if response:
                Say(response)
            if callback:
                callback()
