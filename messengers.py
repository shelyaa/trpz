from abc import ABC, abstractmethod

import requests as reqs


class Messenger(ABC):

    @abstractmethod
    def send_message(self, bot_token, receiver, message_type, message_content):
        pass


class Telegram(Messenger):

    def send_message(self, bot_token, receiver, message):

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

        data = {
            'chat_id': receiver,
            'parse_mode': "Markdown",
            'text': message
        }

        success = reqs.post(url, data=data).json()['ok']

        return success


class Viber(Messenger):

    def send_message(self, bot_token, receiver, message):

        url = "https://chatapi.viber.com/pa/send_message"

        headers = {'X-Viber-Auth-Token': bot_token}

        data = {
            "receiver": receiver,
            "type": "text",
            "text": message
        }

        success = reqs.post(url, headers=headers, json=data).json()['status_message'] == 'ok'

        return success


MESSENGERS = {
    'telegram': Telegram(),
    'viber': Viber()
}
