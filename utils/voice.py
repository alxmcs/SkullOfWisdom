import numpy as np
import pyttsx3
import json
import os


class VoiceEmitter:
    def __init__(self, phrases, unknown, symbol, volume=1.0):
        self.__engine = pyttsx3.init()
        self.__phrases = phrases
        self.__unknown = unknown
        self.__replace_symbol = symbol
        self.__engine.setProperty('volume', volume)
        voices = self.__engine.getProperty('voices')
        self.__engine.setProperty('voice', voices[0].id)

    def play_message(self, text):
        self.__engine.say(text)
        self.__engine.runAndWait()

    def play_greeting(self, name):
        if name is None:
            name = self.__unknown
        self.play_message(np.random.choice(self.__phrases, 1)[0].replace('{x}', name))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.getcwd()), 'settings.json'), encoding="utf-8") as json_file:
        settings = json.load(json_file)
    ve = VoiceEmitter(settings['phrases_list'], settings['unknown_name'], settings['replace_symbol'])
    ve.play_greeting('Лёха')
    ve.play_greeting('Саня')
    ve.play_greeting('Настя')
    ve.play_greeting('Илья')
    ve.play_greeting('Роман')
    ve.play_greeting('Паша')
    ve.play_greeting('Артём')
    ve.play_greeting(None)
