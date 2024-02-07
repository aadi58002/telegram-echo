from dotenv import load_dotenv

import uvicorn
import logging
import httpx

from fastapi import FastAPI, Request, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from utils import getEnv
from telegram import TelegramBot

def registerWebHook(telegram_bot: TelegramBot,publicUrl: str):
    params = {
        'chat_id': telegram_bot.chat_id,
        'url': publicUrl,
    }

    try:
        response = httpx.post(f"{telegram_bot.api_base_url}/setWebhook", data=params)
        response.raise_for_status()
        result = response.json()

        if result['ok']:
            logging.info(f"Webhook setup successfully! for {publicUrl}")
        else:
            logging.error(f"Failed to Webhook Setup. Error: {result['description']}")

    except Exception as e:
        logging.error(f"Error during Webhook setup: {e}")

load_dotenv()
logging.basicConfig(level=logging.INFO)

telegramBot = TelegramBot()
publicUrl = getEnv("PUBLIC_URL")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.error(f"{await request.json()}: {exc_str}")
    content = {'status_code': 422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

def getTelegramBot():
    return TelegramBot()

@app.post("/")
async def getWebHook(request: Request,telegram_bot: TelegramBot = Depends(getTelegramBot)):
    data = await request.json()
    print(f"Received data: {data}")
    telegram_bot.send_message(data['message']['from']['id'],data['message']['text'])
    return JSONResponse(content={}, status_code=200)

registerWebHook(telegramBot,publicUrl)
uvicorn.run(app, port=8000)
