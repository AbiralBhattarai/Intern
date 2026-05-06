from src.ports.output.AiServicePort import AiServicePort
from src.domain.models.CampaignDataInputModel import CampaignDataInput
from src.domain.models.CampaignDataOutputModel import CampaignDataOutput


class CampaignReiterateService:
    """Application Service that orchestrates campaign reiteration."""
    def __init__(self,ai_service: AiServicePort):
        """Initialize with injected AI service dependency."""
        self.ai_service = ai_service
        
        
    def reiterate_campaign(self,critique:CampaignDataOutput,campaign_data:CampaignDataInput) -> CampaignDataInput:
        """Full campaign reiteration flow: generate new campaign based on critique and original data."""
        system_prompt = """You are a world-class marketing and video production expert with brilliant writing skills.
        Your task is make changes to the original campaign based on the provided critique and generate a new improved campaign.
        Please ensure the revised campaign maintains the original goals and messaging while addressing the identified weaknesses.
        """
        user_prompt =  f"""Previous Details:
        
        campaign_data: {campaign_data}
        
        fixes: {critique.fixes}
        
        Please provide the revised campaign details in JSON format with the same structure as the original campaign data.
        Donot Makes changes to the campaign goals, campaign_description, promoting item, nichce ,campaign end date.
        you can suggest changes to the video script, video type, video orientation and video duration if needed.
        """
        
        result = self.ai_service.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )
        
        return result