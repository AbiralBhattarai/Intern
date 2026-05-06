from abc import ABC, abstractmethod


class CampaignAnalyzerPort(ABC):

    @abstractmethod
    def analyze(self, campaign_data: dict) -> dict:
        pass