import os
from dotenv import load_dotenv

from src.domain.models.CampaignDataInputModel import CampaignDataInput
from src.bootstrap import setup_dependencies

load_dotenv()


def AnalyzeAndReiterateCampaign(campaign_input: CampaignDataInput) -> CampaignDataInput:
    """
    Orchestrates the complete campaign analysis and reiteration flow.
    
    For FastAPI endpoint usage (synchronous request/response).
    For event-driven Kafka usage, see main_kafka_orchestrator.py
    """
    campaign_analysis_service, campaign_reiterate_service, _, _ = setup_dependencies()
    
    # Log input
    print(f"Niche: {campaign_input.campaign_niche}")
    print(f"Video Type: {campaign_input.video_type}")
    print(f"Duration: {campaign_input.video_duration_seconds}s")
    
    # Step 1: Analyze campaign
    print("\n🔍 Analyzing campaign...")
    analysis_output = campaign_analysis_service.review_campaign(campaign_input)
    print("✅ Analysis complete")
    
    # Step 2: Reiterate campaign
    print("🔄 Reiterating campaign...")
    revised_campaign = campaign_reiterate_service.reiterate_campaign(
        critique=analysis_output,
        campaign_data=campaign_input
    )
<<<<<<< HEAD
    print("✅ Reiteration complete")
    
    return revised_campaign
=======

    return CampaignDataInput.model_validate(revised_campaign)
>>>>>>> main

