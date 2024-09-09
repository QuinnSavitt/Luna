from Module import Module

class Followup(Module):
    def __init__(self, driver):
        super().__init__("Followup", ["followup test"])
        self.d = driver

    def process(self, text):
        name = " ".split(self.d.FollowUp("What is your name?"))[0]
        return "Hello " + name, self.printName(name)

    def printName(self, name):
        print("The user's name is: " + name)
