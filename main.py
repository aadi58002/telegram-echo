from dotenv import load_dotenv

import uvicorn
import asyncio

from api import app
from telegram import TelegramBot
from utils import get_env


if __name__ == "__main__":
    load_dotenv()

    token = get_env("TELEGRAM_TOKEN")
    chat_id = get_env("TELEGRAM_CHAT_ID")
    public_url = get_env("PUBLIC_URL")
    local_port = int(get_env("LOCAL_PORT"))

    telegramBot = TelegramBot(token,chat_id)

    asyncio.run(telegramBot.register_webhook_async(f"{public_url}:{local_port}"))

    uvicorn.run(app, port=local_port)
