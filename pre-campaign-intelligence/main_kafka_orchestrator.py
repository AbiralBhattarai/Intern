import os
from dotenv import load_dotenv
from confluent_kafka.admin import AdminClient, NewTopic

from src.domain.models.CampaignDataInputModel import CampaignDataInput
from src.bootstrap import setup_dependencies

load_dotenv()


def create_topics():
    """Create required Kafka topics if they don't exist."""
    try:
        admin_client = AdminClient({"bootstrap.servers": "localhost:9092"})
        
        topics_to_create = [
            NewTopic(topic="campaign-input", num_partitions=1, replication_factor=1),
            NewTopic(topic="campaign-analysis", num_partitions=1, replication_factor=1),
            NewTopic(topic="final-campaign", num_partitions=1, replication_factor=1),
            NewTopic(topic="campaign-error", num_partitions=1, replication_factor=1),
        ]
        
        # Get existing topics
        metadata = admin_client.list_topics(timeout=5)
        existing_topics = set(metadata.topics.keys())
        
        # Filter topics that don't exist
        topics_to_create = [t for t in topics_to_create if t.name not in existing_topics]
        
        if topics_to_create:
            print(f"📝 Creating {len(topics_to_create)} topics...")
            fs = admin_client.create_topics(topics_to_create, validate_only=False)
            
            for topic, f in fs.items():
                try:
                    f.result()
                    print(f"   ✅ Created topic: {topic}")
                except Exception as e:
                    print(f"   ⚠️  Topic {topic} already exists or error: {e}")
        else:
            print("✅ All required topics already exist")
    except Exception as e:
        print(f"⚠️  Could not create topics: {e}")


def run_kafka_orchestrator():
    """
    Main orchestration loop.
    Consumes from Kafka, processes through services, and produces results back to Kafka.
    
    Flow:
    1. Consumer reads from "campaign-input" topic
    2. CampaignAnalysisService analyzes & critiques
    3. Orchestrator publishes analysis to "campaign-analysis" topic
    4. CampaignReiterateService revises based on critique
    5. Orchestrator publishes final campaign to "final-campaign" topic
    """
    # Create topics if they don't exist
    create_topics()
    
    campaign_analysis_service, campaign_reiterate_service, publisher, consumer = setup_dependencies()
    
    print("\nStarting Kafka Orchestrator...")
    print("Listening on 'campaign-input' topic...")
    print("(Waiting for messages...)\n")
    
    # CONSUME: Read campaign inputs from Kafka
    for campaign_msg in consumer.consume("campaign-input"):
        try:
            # Parse incoming message
            campaign_input = CampaignDataInput(**campaign_msg)
            
            print(f"\nReceived campaign: {campaign_input.campaign_niche}")
            print(f"   Video Type: {campaign_input.video_type}")
            print(f"   Duration: {campaign_input.video_duration_seconds}s")
            
            # Step 1: Analyze & Critique
            print("Analyzing campaign...")
            analysis_output = campaign_analysis_service.review_campaign(campaign_input)
            
            # PRODUCE: Publish analysis results
            print("Publishing analysis results...")
            publisher.publish("campaign-analysis", {
                "input": campaign_input.model_dump(mode='json'),
                "output": analysis_output.model_dump(mode='json')
            })
            print("Analysis published to 'campaign-analysis' topic")
            
            # Step 2: Reiterate & Improve
            print("Reiterating campaign...")
            revised_campaign = campaign_reiterate_service.reiterate_campaign(
                critique=analysis_output,
                campaign_data=campaign_input
            )
            
            # PRODUCE: Publish final campaign
            print("Publishing revised campaign...")
            publisher.publish("final-campaign", revised_campaign.model_dump(mode='json'))
            print("Revised campaign published to 'final-campaign' topic\n")
            
        except Exception as e:
            print(f"Error processing campaign: {str(e)}")
            import traceback
            traceback.print_exc()
            # Publish error to error topic
            try:
                publisher.publish("campaign-error", {
                    "error": str(e),
                    "message": campaign_msg
                })
            except:
                pass


if __name__ == "__main__":
    run_kafka_orchestrator()
