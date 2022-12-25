from dataclasses import field
from typing import List


import marshmallow_dataclass
from marshmallow_dataclass import dataclass
from marshmallow import EXCLUDE


@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    first_name: str | None
    username: str = ""

    class Meta:
        unknown = EXCLUDE


@dataclass
class Chat:
    id: int
    first_name: str | None
    type: str | None
    username: str = ""

    class Meta:
        unknown = EXCLUDE


@dataclass
class Message:
    message_id: int
    date: int
    text: str | None
    from_: MessageFrom = field(metadata={"data_key": "from"})
    chat: Chat

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = EXCLUDE


@dataclass
class UpdateObj:
    update_id: int
    message: Message

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]

    class Meta:
        unknown = EXCLUDE


get_updates_schema = marshmallow_dataclass.class_schema(GetUpdatesResponse)()
send_message_schema = marshmallow_dataclass.class_schema(SendMessageResponse)()
