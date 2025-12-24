from typing import List
from src.models import Message
from src.interfaces import LLMClient

class ChatService:
    def __init__(self, client: LLMClient, system_prompt: str = "You are a helpful and concise assistant."):
        self.client = client
        self._history: List[Message] = []
        self._add_system_message(system_prompt)

    async def ask(self, user_input: str) -> str:
        user_msg = Message(role="user", content=user_input)
        self._history.append(user_msg)

        response_text = await self.client.send_messages(self._history)

        ai_msg = Message(role="assistant", content=response_text)
        self._history.append(ai_msg)
        return response_text

    def _add_system_message(self, content: str):
        self._history.append(Message(role="system", content=content))

    def get_history_count(self) -> int:
        return len(self._history)