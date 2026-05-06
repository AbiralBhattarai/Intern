import json
from pathlib import Path


def load_dummy_campaign_data():
    """
    Load dummy campaign data from JSON file.
    
    Returns:
        list: List of campaign dictionaries
    """
    json_path = Path(__file__).parent.parent.parent / "dummy_data" / "campaign_dummy_data.json"
    
    with open(json_path, 'r') as f:
        return json.load(f)