"""
Prompts for campaign analysis service.
"""

CAMPAIGN_ANALYSIS_SYSTEM_PROMPT = """You are a world-class marketing and video production expert.
Based on the campaign analysis, provide:
1. Pros: List strengths of the current script
2. Cons: List weaknesses/areas for improvement
3. Fixes: Specific, actionable improvements for each weakness

Format your response as JSON with keys: pros, cons, fixes (each as a list of strings)"""


def get_campaign_analysis_user_prompt(campaign_input, analysis_results: dict) -> str:
    """
    Generate user prompt for campaign analysis.
    
    Args:
        campaign_input: CampaignDataInput object
        analysis_results: Dictionary with analysis metrics
        
    Returns:
        Formatted user prompt string
    """
    return f"""
Campaign Data:
- Campaign Goals: {campaign_input.campaign_goals}
- Promoting Item: {campaign_input.promoting_item}
- Niche: {campaign_input.campaign_niche}
- Campaign End Date: {campaign_input.campaign_end_date}
- Campaign Description: {campaign_input.campaign_description}
- Video Type: {campaign_input.video_type}
- Duration: {campaign_input.video_duration_seconds}s
- Video Orientation: {campaign_input.video_orientation}

Analysis Results:
{analysis_results}

Original Script:
{campaign_input.video_script}

Please provide detailed pros, cons, and fixes based on this data.
Also suggest if any of the input parameters could be optimized for better results.
"""
