"""
Prompts for campaign reiteration service.
"""

CAMPAIGN_REITERATION_SYSTEM_PROMPT = """You are a world-class marketing and video production expert with brilliant writing skills.
Your task is make changes to the original campaign based on the provided critique and generate a new improved campaign.
Please ensure the revised campaign maintains the original goals and messaging while addressing the identified weaknesses.
"""


def get_campaign_reiteration_user_prompt(campaign_data, critique) -> str:
    """
    Generate user prompt for campaign reiteration.
    
    Args:
        campaign_data: CampaignDataInput object
        critique: CampaignDataOutput with analysis and fixes
        
    Returns:
        Formatted user prompt string
    """
    return f"""Previous Details:

campaign_data: {campaign_data}

fixes: {critique.fixes}

Please provide the revised campaign details in JSON format with the same structure as the original campaign data.
Do not make changes to the campaign goals, campaign_description, promoting item, niche, campaign end date, video type, video duration and video orientation.
Only make changes to the video script based on the critique.
"""
