from src.ports.output.AiServicePort import AiServicePort
from src.domain.models.CampaignDataInputModel import CampaignDataInput
from src.domain.models.CampaignDataOutputModel import CampaignDataOutput
from src.application.prompts import (
    CAMPAIGN_REITERATION_SYSTEM_PROMPT,
    get_campaign_reiteration_user_prompt
)
import json

class CampaignReiterateService:
    """Application Service that orchestrates campaign reiteration."""
    def __init__(self, ai_service: AiServicePort):
        """Initialize with injected dependencies."""
        self.ai_service = ai_service
        
        
    def reiterate_campaign(self,critique:CampaignDataOutput,campaign_data:CampaignDataInput) -> CampaignDataInput:
        """Full campaign reiteration flow: generate new campaign based on critique and original data."""
        
        system_prompt = CAMPAIGN_REITERATION_SYSTEM_PROMPT
        user_prompt = get_campaign_reiteration_user_prompt(campaign_data, critique)
        
        result = self.ai_service.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )
        json_str = result[result.find("{"): result.rfind("}") + 1]
        data = json.loads(json_str)
        
        revised_campaign = CampaignDataInput.model_validate(data)
        
        return revised_campaign