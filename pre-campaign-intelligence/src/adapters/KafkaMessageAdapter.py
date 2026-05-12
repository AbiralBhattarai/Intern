from confluent_kafka import Producer, Consumer
from src.ports.output.MessagePublisherPort import MessagePublisherPort
from src.ports.output.MessageConsumerPort import MessageConsumerPort
import json

class KafkaMessagePublisher(MessagePublisherPort):
    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})
    
    def publish(self, topic: str, message: dict) -> None:
        self.producer.produce(topic, json.dumps(message).encode())
        self.producer.flush()

class KafkaMessageConsumer(MessageConsumerPort):
    def __init__(self, bootstrap_servers: str = "localhost:9092", group_id: str = "default"):
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })
    
    def consume(self, topic: str):
        self.consumer.subscribe([topic])
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            yield json.loads(msg.value().decode())