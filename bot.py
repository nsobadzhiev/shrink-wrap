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
