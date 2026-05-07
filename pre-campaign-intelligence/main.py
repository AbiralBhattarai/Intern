from fastapi import FastAPI
from src.domain.models.CampaignDataInputModel import CampaignDataInput
from src.application.services.OrchestrationService import AnalyzeAndReiterateCampaign
app = FastAPI()
@app.get("/health-check")
async def root():
    """Health check endpoint to verify the service is running."""
    return {"message": "Pre-Campaign Intelligence System is running!"}


@app.post('/analyze-campaign')
def analyze_campaign(campaign_data: CampaignDataInput)->CampaignDataInput:
    """Endpoint to analyze campaign data."""
    print(campaign_data)
    try:
        result = AnalyzeAndReiterateCampaign(campaign_data)
    except Exception as e:
        print(f"Error during campaign analysis: {e}")
        raise e
    return CampaignDataInput.model_validate(result)