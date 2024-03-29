import requests

from bot.tg import dc


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        """
        URL метод для запроса к telegram боту

        Args:
            method: какой запрос будет отправлен боту

        Returns:
            str
        """
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int=0, timeout: int=60) -> dc.GetUpdatesResponse:
        """
        Получения входящих обновлений от пользователя.

        Args:
            offset: int
            timeout: int

        Returns:
            GetUpdatesResponse
        """
        url = self.get_url('getUpdates')
        response = requests.get(url, params={"offset": offset, "timeout": timeout})
        print(response.json())
        return dc.GET_UPDATES_SCHEMA.load(response.json())

    def send_message(self, chat_id: int, text: str) -> dc.SendMessageResponse:
        """
        Отправление сообщения пользователю от бота.

        Args:
            chat_id: int
            text: int

        Returns:
            SendMessageResponse
        """
        url = self.get_url('sendMessage')
        response = requests.get(url, params={"chat_id": chat_id, "text": text})
        return dc.SEND_MESSAGE_RESPONSE_SCHEMA.load(response.json())




