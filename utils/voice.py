import pyttsx3
import numpy as np

PHRASES = [
    "Привет {x}",
    "{x} здар'ова заеб'ал",
    "Тебе тут не рады {x}",
    "Шал'ом {x}",
    "Здар'ова {x} как сам",
    "О, это же {x}. Прав'аливай отсюда",
    "Здравствуйте {x}",
    "{x} моё почтение",
    "Cал'ам {x} брат'уха жи да"
]
UNIDENTIFIED_NAME = "неустановленный пидар'ас"


class VoiceEmitter:
    def __init__(self, volume=1.0):
        self.__engine = pyttsx3.init()
        self.__engine.setProperty('volume', volume)  
        voices = self.__engine.getProperty('voices')
        self.__engine.setProperty('voice', voices[0].id)

    def play_message(self, text):
        self.__engine.say(text)
        self.__engine.runAndWait()

    def play_greeting(self, name):
        self.play_message(np.random.choice(PHRASES, 1)[0].replace('{x}', name))


if __name__ == "__main__":
    ve = VoiceEmitter()
    ve.play_greeting('Лёха')
    ve.play_greeting('Саня')
    ve.play_greeting('Настя')
    ve.play_greeting('Илья')
    ve.play_greeting('Роман')
    ve.play_greeting('Паша')
    ve.play_greeting('Артём')
    ve.play_greeting(UNIDENTIFIED_NAME)
