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
from dotenv import load_dotenv
# import random
load_dotenv()


def setup_dependencies():
    """
    Dependency injection setup.
    Initializes all adapters and services with their dependencies.
    """
    # Load configuration
    api_key = os.getenv("GOOGEL_GENERATIVE_AI_API_KEY")
    
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
    
    return campaign_analysis_service


def main():
    """
    Main entry point.
    Flow: Load data -> Validate -> Analyze -> Output
    """
    print("Starting Pre-Campaign Intelligence System...")
    print("=" * 60)
    
    try:
        # Step 1: Load dummy data
        print("\n1. Loading dummy campaign data...")
        campaigns = load_dummy_campaign_data()
        print(f"Loaded {len(campaigns)} campaigns")
        
        # Step 2: Setup services
        print("\n2. Initializing services and adapters...")
        service = setup_dependencies()
        
        # Step 3: Process each campaign
        print("\n3. Analyzing campaigns...\n")
        
        campaign = campaigns[0]  # For demo, we process only the first campaign
        try:
                # Validate input
                campaign_input = CampaignDataInput(
                    campaign_goals=campaign.get('Campaign_goals').lower(),
                    promoting_item=campaign.get('Promoting_item', 'physical product'.lower()),
                    campaign_niche=campaign.get('Campaign_niche').lower(),
                    campaign_end_date=campaign.get('Campaign_End_Date').lower(),
                    campaign_description=campaign.get('Campaign_Description', '').lower(),
                    video_orientation=campaign.get('video_orientation', 'portrait').lower(),
                    video_type=campaign.get('video_type', 'information').lower(),
                    video_duration_seconds=campaign.get('video_duration', '0'),
                    video_script=campaign.get('Video_Script', '')
                )
                
                print(f"Processing Campaign ID: {campaign.get('Campaign_ID')}")
                print(f"  Niche: {campaign_input.campaign_niche}")
                print(f"  Video Type: {campaign_input.video_type}")
                print(f"  Duration: {campaign_input.video_duration_seconds}s")
                
                # Analyze campaign (returns validated CampaignDataOutput)
                result = service.review_campaign(campaign_input)
                
                # Display results
                print("\n  ANALYSIS RESULTS:")
                print(f"  Script Length: {len(result.old_script)} characters")
                print(f"\n  PROS:")
                for pro in result.pros:
                    print(f"    ✓ {pro}")
                print(f"\n  CONS:")
                for con in result.cons:
                    print(f"    ✗ {con}")
                print(f"\n  RECOMMENDED FIXES:")
                for fix in result.fixes:
                    print(f"    → {fix}")
                print()
                
        except ValueError as e:
            print(f"  Error processing campaign: {e}")
        
        print("=" * 60)
        print("Analysis complete!")
        
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
