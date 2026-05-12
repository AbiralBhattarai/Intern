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
def analyze_campaign(campaign_data: CampaignDataInput) -> dict:
    """
    Endpoint to analyze campaign data.
    Publishes campaign to Kafka for async processing by the orchestrator.
    """
    _, _, publisher, _ = setup_dependencies()
    
    print(f"\n📤 Publishing campaign to Kafka queue...")
    print(f"   Niche: {campaign_data.campaign_niche}")
    print(f"   Video Type: {campaign_data.video_type}")
    print(f"   Duration: {campaign_data.video_duration_seconds}s")
    
    # Publish to campaign-input topic (orchestrator will consume this)
    publisher.publish("campaign-input", campaign_data.model_dump(mode='json'))
    
    return {
        "status": "queued",
        "message": f"Campaign '{campaign_data.campaign_niche}' queued for analysis",
        "niche": campaign_data.campaign_niche,
        "video_type": campaign_data.video_type
    }