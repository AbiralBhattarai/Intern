import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from src.utils.get_dummy_campaign_data import load_dummy_campaign_data
from src.domain.models.CampaignDataInputModel import CampaignDataInput
from src.adapters.CampaignAnalyzerAdapter import RuleBasedCampaignAnalyzer
from src.adapters.AiServiceAdapter import GeminiAiServiceAdapter
from src.application.services.CampaignAnalysisService import CampaignAnalysisService
from src.config.hook_words_config import HOOK_WORDS
from src.config.ai_model_config import MODEL
from src.config.cta_words_config import CTA_WORDS
from src.application.services.CampaignReiterateService import CampaignReiterateService
from dotenv import load_dotenv
# import random
load_dotenv()


def setup_dependencies():
    """
    Dependency injection setup.
    Initializes all adapters and services with their dependencies.
    """
    # Load configuration
    api_key = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
    
    # Initialize adapters
    sentiment_analyzer = SentimentIntensityAnalyzer()
    
    campaign_analyzer = RuleBasedCampaignAnalyzer(
        sentiment_analyzer=sentiment_analyzer,
        hook_words=HOOK_WORDS,
        cta_words=CTA_WORDS
    )
    
    ai_service = GeminiAiServiceAdapter(
        api_key=api_key,
        model=MODEL
    )
    
    # Initialize application service
    campaign_analysis_service = CampaignAnalysisService(
        analyzer=campaign_analyzer,
        ai_service=ai_service
    )
    
    campaign_reiterate_service = CampaignReiterateService(
        ai_service=ai_service
    )
    
    return campaign_analysis_service,campaign_reiterate_service


def AnalyzeAndReiterateCampaign(campaign_input: CampaignDataInput) -> CampaignDataInput:
    campaign_analysis_service, campaign_reiterate_service = setup_dependencies()

    # campaign_input is already validated by FastAPI/Pydantic
    print(f"Niche: {campaign_input.campaign_niche}")
    print(f"Video Type: {campaign_input.video_type}")
    print(f"Duration: {campaign_input.video_duration_seconds}s")

    # review_campaign expects a CampaignDataInput (your service does model_dump inside)
    critique = campaign_analysis_service.review_campaign(campaign_input)

    # reiterate_campaign expects CampaignDataInput + CampaignDataOutput
    revised_campaign = campaign_reiterate_service.reiterate_campaign(
        critique=critique,
        campaign_data=campaign_input,
    )

    return CampaignDataInput.model_validate(revised_campaign)

