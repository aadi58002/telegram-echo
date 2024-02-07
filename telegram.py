from utils import getEnv
import httpx

class TelegramBot:
    token: str
    chat_id: str
    api_base_url: str

    def __init__(self):
        self.token = getEnv("TELEGRAM_TOKEN")
        self.chat_id = self.token.split(':')[0]
        self.api_base_url = f"https://api.telegram.org/bot{self.token}"

    def send_message(self,chat_id: str,message: str):
        send_url = f"{self.api_base_url}/sendMessage"
        print(chat_id,message)
        data={ 'chat_id': chat_id, 'text': message }
        with httpx.Client() as client:
            client.post(send_url,data=data)
