import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from dotenv import load_dotenv

import system_prompts
from chat_storage import add_chat_message, chat_for_id, add_bot_message
from gpt import ask_custom_gpt
from telegram_message import convert_chat_message

load_dotenv()  # take environment variables from .env.

TOKEN = os.environ.get("TOKEN")
system_prompt = system_prompts.custom_gpts[os.environ.get("CUSTOM_GPT_NAME", "smart_goals")]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your FastAPI bot 😄")

async def handle_message(update: Update, context):
    chat_id = str(update.message.chat.id)
    message = convert_chat_message(update.message)
    add_chat_message(chat_id, message)
    chat = chat_for_id(chat_id)
    response = ask_custom_gpt(system_prompt, chat)
    add_bot_message(chat_id, response)
    await update.message.reply_text(response)

def get_bot_application():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.initialize()
    return app

class Bot:

    def __init__(self, name: str, desc: str, token: str, prompt: str, webhook: str):
        self.telegram_app = None
        self.name = name
        self.desc = desc
        self.token = token
        self.prompt = prompt
        self.webhook = webhook

    async def start(self, update: Update, context):
        await update.message.reply_text(f"Hello! I'm the {self.name} Telegram bot. I can help you with: {self.desc}")

    async def handle_message(self, update: Update, context):
        chat_id = str(update.message.chat.id)
        message = convert_chat_message(update.message)
        add_chat_message(chat_id, message)
        chat = chat_for_id(chat_id)
        response = ask_custom_gpt(self.prompt, chat)
        add_bot_message(chat_id, response)
        await update.message.reply_text(response)

    async def start_bot(self):
        app = Application.builder().token(self.token).build()
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        await app.initialize()
        await app.start()
        await app.bot.set_webhook(self.webhook)
        self.telegram_app = app
        return app

    async def stop_bot(self):
        await self.telegram_app.stop()
        await self.telegram_app.shutdown()
