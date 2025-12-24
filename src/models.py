from dataclasses import dataclass
from typing import Literal

RoleType = Literal["system", "user", "assistant"]

@dataclass
class Message:
    role: RoleType
    content: str

    def to_dict(self) -> dict:
        """
        Transform object to dict for sending JSON request.
        """
        return {
            "role": self.role,
            "content": self.content
        }