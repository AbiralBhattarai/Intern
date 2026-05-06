from pydantic import BaseModel,Field
from typing import List, Annotated


class CampaignReiterateOutput(BaseModel):
    revised_script: Annotated[str, Field(description="Revised video script after applying fixes and improvements")]
    