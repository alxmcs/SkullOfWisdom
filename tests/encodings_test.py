import os
import json
import unittest
from utils.encodings import FaceEncoder


class FaceEncoderTestCase(unittest.TestCase):

    __settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_settings.json')

    def setUp(self):
        with open(FaceEncoderTestCase.__settings_path, encoding="utf-8") as json_file:
            self.settings = json.load(json_file)
        self.horoscope_parser = FaceEncoder(self.settings['images_path'],
                                            self.settings['names_path'],
                                            self.settings['encodings_path'])

    def test_get_new_images(self):
        pass

    def test_get_new_metadata(self):
        pass

    def test_get_encodings_data(self):
        pass

    def test_generate_encodings(self):
        pass

    def test_write_encodings(self):
        pass


if __name__ == '__main__':
    unittest.main()
