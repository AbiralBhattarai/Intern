from typing import Protocol

class SentimentAnalyzer(Protocol):
    def polarity_scores(self, text: str) -> dict:
        """Calculate polarity scores for the given text. Returns a dictionary with sentiment scores."""
        ...