from telegram import Message

from chat_storage import ChatMessage, ChatMember, ChatMemberType


def convert_chat_message(message: Message) -> ChatMessage:
    user = message.from_user
    chat_member = ChatMember(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        type=ChatMemberType.BOT if user.is_bot else ChatMemberType.USER,
    )
    chat_message = ChatMessage(
        message_id=str(message.message_id),
        text=message.text or "",
        by=chat_member,
        time_received=message.date,
    )
    return chat_message
