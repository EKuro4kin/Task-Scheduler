import os

from .client import TgClient
from .dc import GET_UPDATES_SCHEMA, SEND_MESSAGE_RESPONSE_SCHEMA

tg_client = TgClient(os.environ.get('TG_TOKEN'))

__all__ = ("GET_UPDATES_SCHEMA", "SEND_MESSAGE_RESPONSE_SCHEMA", "tg_client", "TgClient")
