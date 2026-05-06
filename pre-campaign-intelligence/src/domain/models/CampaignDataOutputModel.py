from pydantic import BaseModel, Field
from typing import List, Annotated


class CampaignDataOutput(BaseModel):
    """
    Output model for campaign analysis and review results.
    """
    old_script: Annotated[str, Field(
        description="Original video script before improvements"
    )]
    
    pros: Annotated[List[str], Field(
        description="List of strengths/positive aspects of the campaign script"
    )]
    
    cons: Annotated[List[str], Field(
        description="List of weaknesses/areas for improvement in the script"
    )]
    
    fixes: Annotated[List[str], Field(
        description="List of recommended fixes and improvements to the script"
    )]
