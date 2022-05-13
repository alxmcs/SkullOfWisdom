from imutils.video import VideoStream
import imutils
import time
import pickle
import json
from utils.voice import VoiceEmitter
import face_recognition

SETTINGS_PATH = 'settings.json'


class PiButler:
    def __init__(self, settings_path):
        with open(settings_path, encoding="utf-8") as json_file:
            settings = json.load(json_file)
        self.__data = pickle.loads(open(settings['encodings_path'], "rb").read())
        self.__emitter = VoiceEmitter(settings['phrases_list'], settings['unknown_name'], settings['replace_symbol'])
        self.__vs = VideoStream(src=0).start()

    def run_camera(self):
        time.sleep(2.0)
        while True:
            frame = self.__vs.read()
            frame = imutils.resize(frame, width=500)
            boxes = face_recognition.face_locations(frame)
            encodings = face_recognition.face_encodings(frame, boxes)
            for encoding in encodings:
                matches = face_recognition.compare_faces(self.__data["encodings"], encoding)
                if True in matches:
                    matched = [i for (i, b) in enumerate(matches) if b]
                    counts = {}
                    for i in matched:
                        name = self.__data["names"][i]
                        counts[name] = counts.get(name, 0) + 1
                    name = max(counts, key=counts.get)
                    self.__emitter.play_greeting(name)
                else:
                    self.__emitter.play_greeting(None)
            time.sleep(5.0)


if __name__ == "__main__":
    butler = PiButler(SETTINGS_PATH)
    butler.run_camera()
