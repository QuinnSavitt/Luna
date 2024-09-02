# Base class for all modules
from typing import List


class Module:
    def __init__(self, name: str, triggers: List[str]):
        self.name = name
        self.triggers = triggers

    def followUp(self, text):
        pass