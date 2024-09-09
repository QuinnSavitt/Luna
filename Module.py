# Base class for all modules


class Module:
    def __init__(self, name: str, triggers: list[str]):
        self.name = name
        self.triggers = triggers
