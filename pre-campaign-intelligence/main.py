import asyncio
import uuid
import json
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from src.domain.models.CampaignDataInputModel import CampaignDataInput
from src.bootstrap import setup_dependencies
from src.adapters.KafkaMessageAdapter import KafkaMessageConsumer

load_dotenv()

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=10)


def process_and_wait_blocking(request_id: str, campaign_data: CampaignDataInput, publisher, timeout_seconds: int = 300) -> dict:
    """
    Subscribes to final-campaign FIRST, then publishes campaign.
    This ensures we don't miss the message because consumer is already listening.
    """
    try:
        # Create consumer and subscribe to topic BEFORE publishing
        result_consumer = KafkaMessageConsumer(group_id=f"api-response-{request_id}")
        result_consumer.consumer.subscribe(["final-campaign"])
        print(f"Subscribed to final-campaign topic")
        
        # NOW publish campaign (after subscription is ready)
        print(f"Publishing campaign to campaign-input...")
        campaign_dict = campaign_data.model_dump(mode='json')
        campaign_dict['_request_id'] = request_id
        publisher.publish("campaign-input", campaign_dict)
        print(f"Campaign published, waiting for result...")
        
        # Wait for result message
        while True:
            msg = result_consumer.consumer.poll(timeout=1.0)
            
            if msg is None:
                continue
            if msg.error():
                continue
            
            result_data = json.loads(msg.value().decode())
            print(f"Received result from Kafka")
            return result_data
            
    except Exception as e:
        print(f"Error: {e}")
        raise


@app.get("/health-check")
async def root():
    """Health check endpoint to verify the service is running."""
    return {"message": "Pre-Campaign Intelligence System is running!"}


@app.post('/analyze-campaign')
async def analyze_campaign(campaign_data: CampaignDataInput) -> CampaignDataInput:
    """
    Endpoint to analyze campaign data (async/await).
    
    Flow:
    1. Subscribe to final-campaign topic
    2. Publishes campaign to 'campaign-input' Kafka topic
    3. Waits for orchestrator to process and publish to 'final-campaign' topic
    4. Returns the revised campaign when ready
    """
    request_id = str(uuid.uuid4())[:8]
    
    _, _, publisher, _ = setup_dependencies()
    
    print(f"\nReceived campaign analysis request (ID: {request_id})")
    print(f"Niche: {campaign_data.campaign_niche}")
    print(f"Video Type: {campaign_data.video_type}")
    print(f"Duration: {campaign_data.video_duration_seconds}s")
    
    loop = asyncio.get_event_loop()
    try:
        result_data = await asyncio.wait_for(
            loop.run_in_executor(
                executor, 
                process_and_wait_blocking,
                request_id,
                campaign_data,
                publisher,
                300
            ),
            timeout=310
        )
        
        revised_campaign = CampaignDataInput.model_validate(result_data)
        print(f"Returning revised campaign to client\n")
        return revised_campaign
        
    except asyncio.TimeoutError:
        print(f"Timeout waiting for orchestrator\n")
        raise HTTPException(
            status_code=504,
            detail="Processing timeout - orchestrator did not complete within 5 minutes"
        )
    except Exception as e:
        print(f"Error: {str(e)}\n")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing campaign: {str(e)}"
        )