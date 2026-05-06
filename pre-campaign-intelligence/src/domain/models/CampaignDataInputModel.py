from pydantic import BaseModel, Field, field_validator
from typing import Literal, Union, Annotated
from datetime import datetime


class CampaignDataInput(BaseModel):
    campaign_goals: Annotated[Literal['brand awareness', 'building engagement', 'authentic content'], Field(description="Goal of the campaign")] = None
    promoting_item: Annotated[Literal['physical product', 'online service', 'in-store experience'], Field(description="Type of item being promoted")] = 'physical product'
    campaign_niche: Annotated[str, Field(description="Niche of the campaign")] = 'other'
    campaign_end_date: Annotated[datetime, Field(description="End date of the campaign")] = None
    campaign_description: Annotated[str, Field(description="Description of the campaign")] = ''
    video_orientation: Annotated[Literal['portrait', 'landscape', 'square'], Field(description="Orientation of the video")] = 'portrait'
    video_type: Annotated[Literal['before/after', 'information', 'lifestyle', 'reviews', 'product demo', 'recipes', 'testimonials', 'tutorials', 'unboxing'], Field(description="Type of video content")] = 'information'
    video_duration_seconds: Annotated[Union[int, str], Field(description="Duration of the video in seconds")] = 0
    video_script: Annotated[str, Field(description="Script of the video")] = ''
    
    @field_validator('promoting_item', mode='before')
    def normalize_promoting_item(cls, v):
        """Convert promoting_item to lowercase for case-insensitive matching."""
        if isinstance(v, str):
            return v.lower()
        return v
    
    @field_validator('video_orientation', mode='before')
    def normalize_video_orientation(cls, v):
        """Convert video_orientation to lowercase for case-insensitive matching."""
        if isinstance(v, str):
            return v.lower()
        return v
    
    @field_validator('video_type', mode='before')
    def normalize_video_type(cls, v):
        """Convert video_type to lowercase for case-insensitive matching."""
        if isinstance(v, str):
            return v.lower()
        return v
    
    @field_validator('video_duration_seconds', mode='before')
    def validate_video_duration(cls, v):
        """
        Parse video duration in various formats: 
        - "30" -> 30
        - "5m" -> 300
        - ">5m" -> 300 (approx)
        - "15s" -> 15
        """
        if isinstance(v, int):
            return v
        
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
    