from imutils import paths
import face_recognition
import numpy as np
import logging
import pickle
import json
import cv2
import sys
import os

EXTENSIONS = ['.jpg', '.png', '.bmp', '.gif', '.tiff']


def generate_encodings(image_folder, names_path, encodings_path):
    logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout),
                                  logging.FileHandler(filename=os.path.join(os.path.dirname(os.getcwd()),
                                                                            "Encoding.log"),
                                                      encoding='utf-8', mode='a+')],
                        format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                        datefmt="%m/%d/%Y %I:%M:%S",
                        level=logging.INFO)
    encodings = []
    names = []
    image_paths = list(p for p in paths.list_images(image_folder) if os.path.splitext(p)[1] in EXTENSIONS)
    logging.info(f'Got {len(image_paths)} paths to images')
    with open(names_path, encoding='utf-8') as json_file:
        names_dict = json.loads(json_file.read())
    logging.info(f'Read file:person dictionary of {len(names_dict)} elements')

    if os.path.exists(encodings_path) and os.stat(encodings_path).st_size != 0:
        with open(encodings_path, "rb") as pickle_file:
            data = pickle.loads(pickle_file.read())
        encodings = data["names"]
        names = data["encodings"]
        logging.info(f'Got {len(encodings)} encodings for {len(set(names))} people from {encodings_path}')

    for (i, image_path) in enumerate(image_paths):
        if os.path.splitext(os.path.basename(image_path))[0] in names_dict.keys():
            new_name = names_dict[os.path.splitext(os.path.basename(image_path))[0]]
            with open(image_path, "rb") as f:
                chunk = f.read()
            chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
            image = cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb, model="hog")
            new_encodings = face_recognition.face_encodings(rgb, boxes)
            for encoding in new_encodings:
                encodings.append(encoding)
                names.append(new_name)
                logging.info(f'Added encoding for {new_name}')

    with open(encodings_path, "wb") as pickle_file:
        pickle.dump({"encodings": encodings, "names": names}, pickle_file)
    logging.info(f'{len(encodings)} encodings for {len(set(names))} people saved in {encodings_path}')


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.getcwd()), 'settings.json'), encoding="utf-8") as settings_file:
        settings = json.load(settings_file)
    generate_encodings(os.path.join(os.path.dirname(os.getcwd()), settings['images_path']),
                       os.path.join(os.path.dirname(os.getcwd()), settings['names_path']),
                       os.path.join(os.path.dirname(os.getcwd()), settings['encodings_path']))
