import logging
import os

import litellm
from dotenv import load_dotenv

from bot_limits import increment_limit
from chat_storage import Chat, litellm_chat_history

load_dotenv()
logger = logging.getLogger(__name__)

LLM_MODEL = os.environ.get("MODEL")
API_KEY = os.environ.get("API_KEY")
LLM_API_BASE = os.environ.get("LLM_API_BASE")

litellm.api_key = API_KEY


def ask_custom_gpt(system_prompt: str, chat: Chat) -> str:
    if not increment_limit():
        logger.warning("Bot limit reached - returning error")
        return "Bot daily limit reached - try again tomorrow"
    try:
        response = litellm.completion(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                *litellm_chat_history(chat)
            ],
            api_base=LLM_API_BASE,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"
        return reply
