import httpx

class TelegramBot:
    token: str
    chat_id: str
    api_base_url: str

    def __init__(self,token: str,chat_id: str):
        self.token = token 
        self.chat_id = chat_id 
        self.api_base_url = f"https://api.telegram.org/bot{self.chat_id}:{self.token}"

    async def register_webhook_async(self,public_url: str):
        data = {"url": public_url}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.api_base_url}/setWebhook", json=data)
                response.raise_for_status()
                result = response.json()
                
                if result['ok']:
                    print("Webhook registered successfully!")
                else:
                    print(f"Failed to register webhook. Error: {result['description']}")
            
        except httpx.RequestError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
