import re
import os
import json
from datetime import datetime, timedelta
from telethon.sync import TelegramClient
from telethon.tl.types import InputMessagesFilterEmpty
from telethon.tl.functions.messages import SearchRequest


class HoroscopeParser:
    def __init__(self, channel_name, error_message, api_id, api_hash):
        self.__channel_name = channel_name
        self.__api_id = api_id
        self.__api_hash = api_hash
        self._error_message = error_message

    def request_horoscope(self, sign):
        with TelegramClient('skull_of_wisdom_session', self.__api_id, self.__api_hash) as client:
            channel_entity = client.get_entity(self.__channel_name)
            post = client(SearchRequest(peer=channel_entity,
                                        limit=1,
                                        min_date=datetime.today() - timedelta(days=1),
                                        max_date=datetime.today(),
                                        q=sign,
                                        filter=InputMessagesFilterEmpty(),
                                        offset_id=0,
                                        add_offset=0,
                                        max_id=0,
                                        min_id=0,
                                        hash=0
                                        ))
        if len(post.messages) > 0:
            return f'Ты {sign}. Твой нейро-астрологический прогноз на сегодня! {self.__parse_message(post.messages[0].message, sign)} '
        else:
            return self._error_message

    def __parse_message(self, message, sign):
        m = re.search(f'{sign}: (.+?)\n\n', message)
        if m:
            return m.group(1)
        else:
            return self._error_message


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.getcwd()), 'settings.json'), encoding="utf-8") as json_file:
        settings = json.load(json_file)
    hr = HoroscopeParser(settings['horoscope_channel'], settings['horoscope_error_message'], settings['tg_api_id'],
                         settings['tg_api_hash'])
    res = hr.request_horoscope('Близнецы')
    print(res)
    res = hr.request_horoscope('Водолей')
    print(res)
    res = hr.request_horoscope('Говноед')
    print(res)
