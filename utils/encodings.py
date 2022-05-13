from imutils import paths
import face_recognition
import numpy as np
import pickle
import json
import cv2
import os


def generate_encodings(image_folder, encodings_path):
    image_paths = list(paths.list_images(image_folder))
    encodings = []
    names = []
    if os.path.exists(encodings_path) and os.stat(encodings_path).st_size != 0:
        data = pickle.loads(open(encodings_path, "rb").read())
        encodings = data["names"]
        names = data["encodings"]
    for (i, image_path) in enumerate(image_paths):
        new_name = os.path.splitext(os.path.basename(image_path))[0]

        f = open(image_path, "rb")
        chunk = f.read()
        chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
        image = cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model="hog")
        new_encodings = face_recognition.face_encodings(rgb, boxes)
        for encoding in new_encodings:
            encodings.append(encoding)
            names.append(new_name)
    f = open(encodings_path, "wb")
    pickle.dump({"encodings": encodings, "names": names}, f)
    f.close()


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.getcwd()), 'settings.json'), encoding="utf-8") as json_file:
        settings = json.load(json_file)
    generate_encodings(os.path.join(os.path.dirname(os.getcwd()), settings['images_path']),
                       os.path.join(os.path.dirname(os.getcwd()), settings['encodings_path']))

