import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from telegram import Update

from bot import Bot
from config import BotSettings, BotConfig
from system_prompts import custom_gpts

load_dotenv()  # take environment variables from .env.

DOMAIN = os.environ.get("DOMAIN")

config = BotSettings()
bots = []

def _webhook_for_bot(name: str) -> str:
    return f'https://{DOMAIN}/webhook/{name}'


def _bot_for_settings(settings: BotConfig) -> Bot:
    return Bot(
        name=settings.name,
        token=settings.token,
        prompt=custom_gpts[settings.system_prompt],
        webhook=_webhook_for_bot(settings.name),
        desc="",
    )


def _bot_for_name(name: str) -> Bot | None:
    for bot in bots:
        if bot.name == name:
            return bot
    return None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global bots
    bots = [_bot_for_settings(bot_settings) for bot_settings in config.bots]
    [await bot.start_bot() for bot in bots]

    print("Bot initialized and webhook set.")
    yield

    # Shutdown
    [await bot.stop_bot() for bot in bots]
    print("Bot stopped and cleaned up.")


app = FastAPI(lifespan=lifespan)


@app.post("/webhook/{bot}")
async def telegram_webhook(bot: str, req: Request):
    bot = _bot_for_name(bot)
    data = await req.json()
    update = Update.de_json(data, bot.telegram_app.bot)
    await bot.telegram_app.process_update(update)
    return {"ok": True}
