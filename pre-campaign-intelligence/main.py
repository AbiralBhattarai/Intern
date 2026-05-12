from fastapi import FastAPI
from dotenv import load_dotenv
from src.domain.models.CampaignDataInputModel import CampaignDataInput
from src.bootstrap import setup_dependencies

load_dotenv()

app = FastAPI()

@app.get("/health-check")
async def root():
    """Health check endpoint to verify the service is running."""
    return {"message": "Pre-Campaign Intelligence System is running!"}


@app.post('/analyze-campaign')
def analyze_campaign(campaign_data: CampaignDataInput) -> CampaignDataInput:
    """
    Endpoint to analyze campaign data.
    Returns revised campaign immediately AND publishes to Kafka for background processing.
    """
    campaign_analysis_service, campaign_reiterate_service, publisher, _ = setup_dependencies()
    
    print(f"\n📥 Processing campaign synchronously: {campaign_data.campaign_niche}")
    print(f"   Video Type: {campaign_data.video_type}")
    print(f"   Duration: {campaign_data.video_duration_seconds}s")
    
    # Step 1: Analyze campaign
    print("🔍 Analyzing campaign...")
    analysis_output = campaign_analysis_service.review_campaign(campaign_data)
    
    # Step 2: Reiterate campaign
    print("🔄 Reiterating campaign...")
    revised_campaign = campaign_reiterate_service.reiterate_campaign(
        critique=analysis_output,
        campaign_data=campaign_data
    )
    print("✅ Analysis complete, returning result")
    
    # ALSO publish to Kafka for orchestrator to process in background
    print("📤 Publishing to Kafka for background processing...")
    publisher.publish("campaign-input", campaign_data.model_dump(mode='json'))
    
    return revised_campaign