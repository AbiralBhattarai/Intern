from src.ports.input.CampaignAnalyzerPort import CampaignAnalyzerPort
from src.ports.output.AiServicePort import AiServicePort
from src.domain.models.CampaignDataInputModel import CampaignDataInput
from src.domain.models.CampaignDataOutputModel import CampaignDataOutput
from src.application.prompts import (
    CAMPAIGN_ANALYSIS_SYSTEM_PROMPT,
    get_campaign_analysis_user_prompt
)
import json


class CampaignAnalysisService:
    """
    Application Service that orchestrates campaign analysis.
    Uses CampaignAnalyzer for metrics and AI service for critique.
    """

    def __init__(
        self,
        analyzer: CampaignAnalyzerPort,
        ai_service: AiServicePort
    ):
        """
        Initialize with injected dependencies.
        
        Args:
            analyzer: Campaign analyzer port (implementation)
            ai_service: AI service port (implementation)
        """
        self.analyzer = analyzer
        self.ai_service = ai_service

    def review_campaign(
        self,
        campaign_input: CampaignDataInput
    ) -> CampaignDataOutput:
        """
        Full campaign review flow: analyze -> critique -> output.
        
        Args:
            campaign_input: Validated campaign data input
            
        Returns:
            CampaignDataOutput: Validated output with pros, cons, fixes
        """
        # Step 1: Analyze campaign with rule-based analyzer
        campaign_dict = campaign_input.model_dump()
        print(campaign_dict)
        analysis_results = self.analyzer.analyze(campaign_dict)
        
        # Step 2: Generate AI critique based on analysis
        system_prompt = CAMPAIGN_ANALYSIS_SYSTEM_PROMPT
        user_prompt = get_campaign_analysis_user_prompt(campaign_input, analysis_results)
        
        critique = self.ai_service.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )
        
        # Step 3: Parse AI response
        try:
            json_start = critique.find('{')
            json_end = critique.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = critique[json_start:json_end]
                critique_data = json.loads(json_str)
            else:
                raise json.JSONDecodeError("No JSON found", critique, 0)
            
            pros = critique_data.get('pros', [])
            cons = critique_data.get('cons', [])
            fixes = critique_data.get('fixes', [])
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing JSON: {e}")
            print(f"Raw response: {critique}")
            # If parsing fails, use defaults
            pros = ["Well-structured script"]
            cons = ["Consider adding more engagement hooks"]
            fixes = ["Incorporate emotional triggers"]
        
        output = CampaignDataOutput(
            old_script=campaign_input.video_script,
            pros=pros,
            cons=cons,
            fixes=fixes
        )
        
        return output