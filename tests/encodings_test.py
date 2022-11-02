import os
import json
import unittest
from utils.encodings import FaceEncoder


class FaceEncoderTestCase(unittest.TestCase):
    __settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_settings.json')

    def setUp(self):
        with open(FaceEncoderTestCase.__settings_path, encoding="utf-8") as json_file:
            self.__settings = json.load(json_file)
        self.__face_encoder = FaceEncoder(
            os.path.join(os.path.dirname(self.__settings_path), self.__settings['images_path']),
            os.path.join(os.path.dirname(self.__settings_path), self.__settings['names_path']),
            os.path.join(os.path.dirname(self.__settings_path), self.__settings['encodings_path']))

    def test_get_new_images(self):
        image_paths = self.__face_encoder._get_new_images()
        self.assertIsNotNone(image_paths)
        self.assertEqual(1, len(image_paths))
        self.assertIsNotNone(image_paths[0])
        self.assertEqual(
            os.path.join(os.path.dirname(self.__settings_path), 'test_image.jpg'),
            image_paths[0])

    def test_get_new_metadata(self):
        metadata = self.__face_encoder._get_new_metadata()
        self.assertIsNotNone(metadata)
        self.assertEqual(1, len(metadata))
        self.assertEqual('test_image', list(metadata.keys())[0])
        self.assertEqual(2, len(metadata['test_image']))
        self.assertEqual('name', list(metadata['test_image'].keys())[0])
        self.assertEqual('sign', list(metadata['test_image'].keys())[1])
        self.assertEqual('Tony', metadata['test_image']['name'])
        self.assertEqual("Don't care", metadata['test_image']['sign'])

    def test_get_encodings_data(self):
        encodings, metadata = self.__face_encoder._get_encodings_data()
        self.assertIsNotNone(encodings)
        self.assertEqual(1, len(encodings))
        self.assertEqual(0, encodings[0])
        self.assertIsNotNone(metadata)
        self.assertEqual(1, len(metadata))
        self.assertIsNotNone(metadata[0])
        self.assertEqual(2, len(list(metadata[0].keys())))
        self.assertEqual('name', list(metadata[0].keys())[0])
        self.assertEqual('sign', list(metadata[0].keys())[1])
        self.assertEqual('test_name', metadata[0]['name'])
        self.assertEqual('test_sigh', metadata[0]['sign'])


if __name__ == '__main__':
    unittest.main()
