from Module import Module


class Test(Module):
    def __init__(self):
        super().__init__("test", ["test"])
        self.state = "hello"

    def process(self, text):
        print("processing")
        if "modify" in text:
            if self.state == "hello":
                self.state = "hi"
            else:
                self.state = "hello"
            return None, None
        else:
            # returns the pre-run response, and a callback function to actually run the process
            return [self.state, self.run]

    def run(self):
        print("I'm a callback function")
