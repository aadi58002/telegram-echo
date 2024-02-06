from fastapi import FastAPI, Request

from telegram import TelegramBot
from utils import get_env

import httpx

app = FastAPI()

@app.post("/")
async def set_webhook(request: Request):
    data = await request.json()
    webhook_url = data.get("webhook_url")
    
    token = get_env("TELEGRAM_TOKEN")
    chat_id = get_env("TELEGRAM_CHAT_ID")

    telegramBot = TelegramBot(token,chat_id)

    send_url = f"{telegramBot.api_base_url}/sendMessage"

    params = {
        'chat_id': chat_id,
        'text': webhook_url,
    }

    try:
        with httpx.Client() as client:
            response = client.post(send_url, data=params)
            response.raise_for_status()
            result = response.json()

            if result['ok']:
                print("Message sent successfully!")
            else:
                print(f"Failed to send message. Error: {result['description']}")

    except httpx.RequestError as e:
        print(f"Request error: {e}")
