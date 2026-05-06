from abc import ABC, abstractmethod


class CampaignAnalyzerPort(ABC):
    """Port for campaign analysis. Defines the interface for analyzing campaign data."""
    @abstractmethod
    def analyze(self, campaign_data: dict) -> dict:
        pass