from imutils.video import VideoStream
import imutils
import time
import pickle
from utils.voice import VoiceEmitter, UNIDENTIFIED_NAME
from utils.encodings import ENCODINGS_PATH
import face_recognition


class PiButler:
    def __init__(self, path):
        self.__data = pickle.loads(open(path, "rb").read())
        self.__emitter = VoiceEmitter()
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
                    self.__emitter.play_greeting(UNIDENTIFIED_NAME)
            time.sleep(5.0)


if __name__ == "__main__":
    butler = PiButler(ENCODINGS_PATH)
    butler.run_camera()