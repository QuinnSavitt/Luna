from Modules.Spotify import Spotify
from Modules.Weather import Weather
from Modules.Sports import Sports
from Envs import *

# Initiate modules. Note that overlaps will be handled by priority in this list
tenv = Tenv()
modules = [Spotify(), Weather(), Sports(tenv)]
triggers = {}
for m in modules:
    for t in m.triggers:
        if t not in triggers.keys():
            triggers[t] = m

def FindModule(text):
    for tr, mo in triggers.items():
        if tr in text:
            print("Identified module: ", mo.name)
            return mo.process(text)
    return "Couldn't locate module, trying again", None

while True:
    command = input("cmd: ")
    response, callback = FindModule(command)
    if response:
        print(response)
    if callback:
        callback()
