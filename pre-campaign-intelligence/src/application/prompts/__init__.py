"""
Centralized prompt templates for AI services.
All prompts should be defined here and imported where needed.
"""

from .campaign_analysis_prompts import (
    CAMPAIGN_ANALYSIS_SYSTEM_PROMPT,
    get_campaign_analysis_user_prompt
)
from .campaign_reiteration_prompts import (
    CAMPAIGN_REITERATION_SYSTEM_PROMPT,
    get_campaign_reiteration_user_prompt
)

__all__ = [
    'CAMPAIGN_ANALYSIS_SYSTEM_PROMPT',
    'get_campaign_analysis_user_prompt',
    'CAMPAIGN_REITERATION_SYSTEM_PROMPT',
    'get_campaign_reiteration_user_prompt',
]
