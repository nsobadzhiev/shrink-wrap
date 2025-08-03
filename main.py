import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from telegram import Update

from bot import get_bot_application

load_dotenv()  # take environment variables from .env.

DOMAIN = os.environ.get("DOMAIN")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await bot_app.initialize()
    await bot_app.start()

    # Set webhook
    webhook_url = f"https://{DOMAIN}/webhook"
    await bot_app.bot.set_webhook(webhook_url)

    print("Bot initialized and webhook set.")
    yield

    # Shutdown
    await bot_app.stop()
    await bot_app.shutdown()
    print("Bot stopped and cleaned up.")


app = FastAPI(lifespan=lifespan)
bot_app = get_bot_application()


@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return {"ok": True}

@app.get("/")
def home():
    return {"message": "Telegram Bot is running"}
