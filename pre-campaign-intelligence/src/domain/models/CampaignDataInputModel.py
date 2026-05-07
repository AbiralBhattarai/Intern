from typing import Annotated, Union
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from src.domain.models.enums import CampaignGoal, PromotingItem, VideoOrientation, VideoType


class CampaignDataInput(BaseModel):
    campaign_goals: Annotated[CampaignGoal | None, Field(description="Goal of the campaign")] = None
    promoting_item: Annotated[PromotingItem, Field(description="Type of item being promoted")] = PromotingItem.PHYSICAL_PRODUCT
    campaign_niche: Annotated[str, Field(description="Niche of the campaign")] = "other"
    campaign_end_date: Annotated[datetime | None, Field(description="End date of the campaign")] = None
    campaign_description: Annotated[str, Field(description="Description of the campaign")] = ""
    video_orientation: Annotated[VideoOrientation, Field(description="Orientation of the video")] = VideoOrientation.PORTRAIT
    video_type: Annotated[VideoType, Field(description="Type of video content")] = VideoType.INFORMATION
    video_duration_seconds: Annotated[Union[int, str], Field(description="Duration of the video in seconds")] = 0
    video_script: Annotated[str, Field(description="Script of the video")] = ""
    
    @field_validator('promoting_item', mode='before')
    def normalize_promoting_item(cls, v:str):
        """Convert promoting_item to lowercase for case-insensitive matching."""
        return v.lower()
    
    @field_validator('video_orientation', mode='before')
    def normalize_video_orientation(cls, v:str):
        """Convert video_orientation to lowercase for case-insensitive matching."""
        return v.lower()
    
    @field_validator('video_type', mode='before')
    def normalize_video_type(cls, v:str):
        """Convert video_type to lowercase for case-insensitive matching."""
        return v.lower()
    
    @field_validator('video_duration_seconds', mode='before')
    def validate_video_duration(cls, v: Union[int, str]):
        """
        Parse video duration in various formats: 
        - "30" -> 30
        - "5m" -> 300
        - ">5m" -> 300 (approx)
        - "15s" -> 15
        """
        if v is None:
            return 0
        
        if isinstance(v, (int,float)):
            return int(v)
        
        if isinstance(v, str):
            v = v.strip()
            
            # Handle formats like ">5m", "~30s", etc
            if v and v[0] in ['>', '<', '~', '+', '-']:
                v = v[1:].strip()
            
            # Extract numeric part
            digits = ''
            for ch in v:
                if ch.isdigit() or ch == '.':
                    digits += ch
                else:
                    break
            
            if not digits:
                raise ValueError(f"Invalid video duration: {v}")
            
            duration = float(digits)
            
            # Check for time unit suffix
            remaining = v[len(digits):].strip().lower()
            
            if remaining.startswith('m'):  # minutes
                duration = int(duration * 60)
            elif remaining.startswith('h'):  # hours
                duration = int(duration * 3600)
            elif remaining.startswith('s'):  # seconds
                duration = int(duration)
            else:
                # Assume seconds if no unit specified
                duration = int(duration)
            
            return duration
        
        return v
    