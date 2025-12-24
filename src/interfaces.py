from abc import ABC, abstractmethod
from typing import List
from src.models import Message

class LLMClient(ABC):
    """
    Abstract class for LLM client
    """

    @abstractmethod
    async def send_messages(self, message: List[Message]) -> str:
        """
        Sends history of messages to LLM and returns the response
        Args:
            message (List[Message]): List of messages to send to LLM
        Returns:
            str: Response from LLM
        """
        pass