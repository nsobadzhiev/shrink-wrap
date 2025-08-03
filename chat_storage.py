from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

class ChatMemberType(Enum):
    BOT = "bot"
    USER = "user"

class ChatMember(BaseModel):
    id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    type: ChatMemberType

class ChatMessage(BaseModel):
    message_id: str
    text: str
    by: ChatMember
    time_received: datetime

class Chat(BaseModel):
    chat_id: str
    messages: list[ChatMessage]


chats: dict[str, Chat] = {}


def add_message(chat_id: str, message_id: str, message: str, by: ChatMember, time: datetime):
    chat = chats[chat_id] if chat_id in chats else Chat(chat_id=chat_id, messages=[])
    chat_message = ChatMessage(message_id=message_id, text=message, by=by, time_received=time)
    chat.messages.append(chat_message)


def add_chat_message(chat_id: str, message: ChatMessage) -> ChatMessage:
    chat = chats[chat_id] if chat_id in chats else Chat(chat_id=chat_id, messages=[])
    chats[chat_id] = chat
    chat.messages.append(message)
    return message


def add_bot_message(chat_id: str, response: str) -> ChatMessage:
    message = ChatMessage(
        message_id='',
        text=response,
        by=ChatMember(
            id=1,
            type=ChatMemberType.BOT
        ),
        time_received=datetime.now()
    )
    return add_chat_message(chat_id, message)


def chat_for_id(chat_id: str) -> Optional[Chat]:
    return chats[chat_id] if chat_id in chats else None


def litellm_chat_history(chat: Chat) -> list[dict[str, str]]:
    return [{
        "role": "user" if message.by.type == ChatMemberType.USER else "assistant",
        "content": message.text} for message in chat.messages
    ]
