from collections import deque


class Env:
    def __init__(self):
        self.warnings = deque()
        self.errors = deque()
        self.logs = deque()

    def log(self, text):
        self.logs.append(text)
        if len(self.logs) > 50:
            self.logs.popleft()

    def awaitB(self):
        return input("-") in "ty1"

    def flag(self, text):
        self.warnings.append(text)

    def throw(self, text):
        self.errors.append(text)
        self.log(text)

    def getFlag(self):
        self.log(a := self.warnings.popleft())
        self.log("Keep?")
        if self.awaitB():
            self.warnings.append(a)

    def getError(self):
        self.log(a := self.errors.popleft())
        self.log("Keep?")
        if self.awaitB():
            self.errors.append(a)


class Tenv(Env):
    def __init__(self):
        super().__init__()

    def flag(self, text):
        super().flag(text)
        print(text)

    def throw(self, text):
        super().throw(text)
        print(text)


class DevEnv(Env):
    def __init__(self):
        super().__init__()

    def log(self, text):
        super().log(text)
        print(text)

    def flag(self, text):
        super().flag(text)
        print(text)

    def throw(self, text):
        super().throw(text)
        print(text)