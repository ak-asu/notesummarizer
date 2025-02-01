import pyttsx3
import threading
from collections import OrderedDict


class Voiceover:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Voiceover, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.engine = pyttsx3.init()
        self.voices = OrderedDict((voice.name, voice.id) for voice in self.engine.getProperty('voices'))

    def output_voiceover(self, text, voice_option):
        def run():
            voice_id = self.voices.get(voice_option, None)
            if voice_id:
                self.engine.setProperty('voice', voice_id)
            else:
                raise ValueError(f"Voice option '{voice_option}' not found.")
            self.engine.say(text)
            if self.engine._inLoop:
                self.engine.endLoop()
            else:
                self.engine.runAndWait()
            self.engine.stop()
        thread = threading.Thread(target=run)
        thread.start()
