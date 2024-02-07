import logging
import uvicorn

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from telegramBot import TelegramBot

app = FastAPI()
templates = Jinja2Templates(directory="templates")
list_processes = dict()

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit/")
async def submit_form(request: Request):
    data = (await request.json())['input_text']
    logging.info(data)
    if not data in list_processes:
        telegramBot = TelegramBot(data)
        telegramBot.start()
        logging.info("Telebot started")
        list_processes[data] = telegramBot
        return "Successfully registered bot"
    else:
        return "Already registered bot"

uvicorn.run(app,port=8000)
