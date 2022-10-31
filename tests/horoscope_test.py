import json
import unittest
from utils.horoscope import HoroscopeParser


class HoroscopeParserTestCase(unittest.TestCase):

    __settings_path = 'test_settings.json'

    def setUp(self):
        with open(HoroscopeParserTestCase.__settings_path, encoding="utf-8") as json_file:
            self.settings = json.load(json_file)
        self.horoscope_parser = HoroscopeParser(self.settings['horoscope_channel'],
                                                self.settings['horoscope_error_message'],
                                                self.settings['tg_api_id'],
                                                self.settings['tg_api_hash'])

    def test_request_horoscope_correct_sign(self):
        self.assertNotEqual(self.horoscope_parser._error_message, self.horoscope_parser.request_horoscope('Рак'))

    def test_request_horoscope_wrong_sign(self):
        self.assertEqual(self.horoscope_parser._error_message, self.horoscope_parser.request_horoscope('Краб'))


if __name__ == '__main__':
    unittest.main()
