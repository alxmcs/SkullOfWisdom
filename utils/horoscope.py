import requests
import json
import os
from telethon.tl.functions.contacts import ResolveUsernameRequest

class HoroscopeRequester:
    def __init__(self, base_url, error_message):
        self.__base_url = base_url
        self._error_message = error_message

    def request_horoscope(self, sign):
        response = requests.get(f"{self.__base_url}{sign}")
        if response.status_code == 200:
            return response.json()['horoscope']
        else:
            return self._error_message


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.getcwd()), 'settings.json'), encoding="utf-8") as json_file:
        settings = json.load(json_file)
    hr = HoroscopeRequester(settings['horoscope_api'], settings['horoscope_error_message'])
    print(hr.request_horoscope('aquarius'))
    print(hr.request_horoscope('gemini'))
