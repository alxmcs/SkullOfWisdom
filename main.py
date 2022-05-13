from imutils.video import VideoStream
from utils.voice import VoiceEmitter
import face_recognition
import logging
import imutils
import pickle
import json
import time

SETTINGS_PATH = 'settings.json'


class PiButler:
    def __init__(self, settings_path):
        logging.basicConfig(handlers=[logging.FileHandler(filename="PiButler.log",
                                                          encoding='utf-8', mode='a+')],
                            format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                            datefmt="%m/%d/%Y %I:%M:%S",
                            level=logging.INFO)
        logging.info('Begin initialization')
        with open(settings_path, encoding="utf-8") as json_file:
            settings = json.load(json_file)
        self.__timeout = settings['timeout']
        logging.info('Settings read')
        self.__data = pickle.loads(open(settings['encodings_path'], "rb").read())
        logging.info('Encodings read')
        self.__emitter = VoiceEmitter(settings['phrases_list'], settings['unknown_name'], settings['replace_symbol'])
        self.__emitter.play_message(settings['startup_message'])
        logging.info('Text-to-speech initialized')
        self.__vs = VideoStream(src=0).start()
        logging.info('Video stream capture started')

    def run_camera(self):
        time.sleep(2.0)
        while True:
            frame = self.__vs.read()
            frame = imutils.resize(frame, width=500)
            boxes = face_recognition.face_locations(frame)
            encodings = face_recognition.face_encodings(frame, boxes)
            logging.info(f'got {boxes.count()} faces')
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
                    logging.info(f'recognized {name}')
                else:
                    self.__emitter.play_greeting(None)
                    logging.info('unknown person appeared')
            time.sleep(self.__timeout)


if __name__ == "__main__":
    butler = PiButler(SETTINGS_PATH)
    butler.run_camera()
