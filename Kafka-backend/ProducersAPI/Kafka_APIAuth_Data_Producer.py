import time
from confluent_kafka import Producer
import requests
import json

# Get user inputs
kafka_broker = "localhost:9092"
api_url = input("Enter the URL of the API: ")
api_auth_key = input("Enter the API auth key: ")
kafka_broker = input("Enter the Kafka broker (format - localhost:9092): ") or kafka_broker
kafka_topic = input("Enter the Kafka topic: ")

# Create a producer to send data to Kafka
producer = Producer({
    'bootstrap.servers': kafka_broker,
    'enable.idempotence': True,
    'queue.buffering.max.messages': 10000000,  # Set the desired queue size
    'queue.buffering.max.ms': 500,
    'compression.type': 'zstd',  # 'gzip' Or 'snappy', 'lz4', 'zstd'
    'acks': 'all'  # or '0' or '1' or '-1'/ 'all'
})

def get_api_data(api_url, api_auth_key):
    headers = {'Authorization': f'Bearer {api_auth_key}'}
    response = requests.get(api_url, headers=headers)

    # Raise an error if the request was unsuccessful
    response.raise_for_status()

    return response.json()

def publish_to_kafka(data):
    # Serialize the message to JSON
    message_json = json.dumps(data)

    # Send the message to Kafka
    producer.produce(topic=kafka_topic, value=message_json)

    # Flush the producer
    producer.flush()

while True:
    # Get the data from the API
    data = get_api_data(api_url, api_auth_key)

    # Publish the data to Kafka
    publish_to_kafka(data)

    # Wait for a while before polling the API again
    time.sleep(10)
