import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass(frozen=True)
class Config:
    """
    Immutable config class
    """
    api_key: str
    model: str

    @staticmethod
    def load() -> 'Config':
        api_key = os.getenv("OPENROUTER_API_KEY")
        model = os.getenv("OPENROUTER_MODEL", "google/gemma-2-9b-it:free")

        if not api_key:
            raise ValueError("API key is required")

        return Config(api_key=api_key, model=model)