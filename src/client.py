import httpx
from typing import List
from src.interfaces import LLMClient
from src.models import Message

class OpenRouterClient(LLMClient):
    """
    Client implementation for OpenRouter
    """

    def __init__(self, api_key: str, model: str = "google/gemma-2-9b-it:free"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

    async def send_messages(self, messages: List[Message]) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages_payload = [msg.to_dict() for msg in messages]

        data = {
            "model": self.model,
            "messages": messages_payload
        }

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(self.api_url, headers=headers, json=data)
                response.raise_for_status()
                json_response = response.json()

                content = json_response["choices"][0]["message"]["content"]
                return content

        except httpx.HTTPStatusError as e:
            return f"API Error {e.response.status_code}: {e.response.text}"
        except httpx.RequestError as e:
            return f"Network Error: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"Parsing Error: {str(e)}"