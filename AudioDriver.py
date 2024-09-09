import speech_recognition as sr
import pyttsx3 as tts


class AudioDriver:
    def __init__(self):
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()

    def Listen(self):
        with self.mic as source:
            self.r.adjust_for_ambient_noise(source, 0.1)
            audio = self.r.listen(source, timeout=5, phrase_time_limit=4)
            command = ""

            try:
                command = self.r.recognize_google(audio)
                print(command)
            except Exception as e:
                print("Exception: " + str(e))

            return command.lower()

    def Say(self, text: str):
        engine = tts.init()
        engine.say(text)
        engine.runAndWait()

    def FollowUp(self, text: str):
        self.Say(text)
        return self.Listen()
