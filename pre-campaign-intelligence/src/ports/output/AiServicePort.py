from abc import ABC, abstractmethod


class AiServicePort(ABC):
    """Port for AI service. Defines the interface for generating content using AI."""
    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        pass