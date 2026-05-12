from abc import ABC, abstractmethod
from typing import Iterator

class MessageConsumerPort(ABC):
    """Port for consuming messages from external systems."""
    @abstractmethod
    def consume(self, topic: str) -> Iterator[dict]:
        pass