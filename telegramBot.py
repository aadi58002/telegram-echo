import logging
from multiprocessing import Process

from telegram import Update
from telegram.ext import Application,ApplicationBuilder, MessageHandler, filters

async def echo(update: Update,_) -> None:
    message = update.message.text
    await update.message.reply_text(message)

class TelegramBot:
    app: Application

    def __init__(self,token: str) -> None:
        logging.info(f"Starting bot for {token}")
        self.app = ApplicationBuilder().token(token).build()
        self.app.add_handler(MessageHandler(filters.TEXT, echo))

    def start(self) -> Process:
        p = Process(target=self.app.run_polling,args=())
        p.start()
        return p

