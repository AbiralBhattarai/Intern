"""
Bootstrap module for dependency injection setup.
Centralizes all dependency wiring in one place.
Respects hexagonal architecture: services depend on ports, not implementations.
"""
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from src.adapters.CampaignAnalyzerAdapter import RuleBasedCampaignAnalyzer
from src.adapters.AiServiceAdapter import GeminiAiServiceAdapter
from src.adapters.KafkaMessageAdapter import KafkaMessagePublisher, KafkaMessageConsumer
from src.application.services.CampaignAnalysisService import CampaignAnalysisService
from src.application.services.CampaignReiterateService import CampaignReiterateService
from src.config.hook_words_config import HOOK_WORDS
from src.config.ai_model_config import MODEL
from src.config.cta_words_config import CTA_WORDS


def setup_dependencies():
    """
    Dependency injection setup.
    Initializes all adapters and services with their dependencies.
    Services depend on ports (abstractions), not on Kafka directly.
    
    Returns:
        Tuple of (CampaignAnalysisService, CampaignReiterateService, 
        MessagePublisherPort, MessageConsumerPort)
    """
    # Load configuration
    api_key = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
    
    # Initialize infrastructure adapters (Kafka ports)
    sentiment_analyzer = SentimentIntensityAnalyzer()
    publisher = KafkaMessagePublisher()
    consumer = KafkaMessageConsumer()
    
    # Initialize domain adapters
    campaign_analyzer = RuleBasedCampaignAnalyzer(
        sentiment_analyzer=sentiment_analyzer,
        hook_words=HOOK_WORDS,
        cta_words=CTA_WORDS
    )
    
    ai_service = GeminiAiServiceAdapter(
        api_key=api_key,
        model=MODEL
    )
    
    # Initialize application services with injected ports
    campaign_analysis_service = CampaignAnalysisService(
        analyzer=campaign_analyzer,
        ai_service=ai_service
    )
    
    campaign_reiterate_service = CampaignReiterateService(
        ai_service=ai_service
    )
    
    return campaign_analysis_service, campaign_reiterate_service, publisher, consumer
