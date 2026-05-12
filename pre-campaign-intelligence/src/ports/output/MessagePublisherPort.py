from abc import ABC, abstractmethod

class MessagePublisherPort(ABC):
    """Port for publishing messages to external systems."""
    @abstractmethod
    def publish(self, topic: str, message: dict) -> None:
        pass