import time
import random
import json
from confluent_kafka import Producer
from datetime import datetime

# Get user inputs
kafka_broker = "localhost:9092"
kafka_broker = input("Enter the Kafka broker (format - localhost:9092): ") or kafka_broker
kafka_topic = input("Enter the Kafka topic: ")
num_sensors = int(input("Enter the number of sensors to generate data for: "))

# Create a producer to send data to Kafka
producer = Producer({
    'bootstrap.servers': kafka_broker,
    'enable.idempotence': True,
    'queue.buffering.max.messages': 10000000,  # Set the desired queue size
    'queue.buffering.max.ms': 500,
    'compression.type': 'zstd',  # 'gzip' Or 'snappy', 'lz4', 'zstd'
    'acks': 'all'  # or '0' or '1' or '-1'/ 'all'
})

while True:
    try:
        for i in range(num_sensors):
            sensor_name = f'sensor_{i}'
            timestamp = datetime.utcnow().isoformat()
            value = random.random()  # Generate a random float between 0 and 1

            # Create a message to be sent to Kafka
            message = {
                'timestamp': timestamp,
                'sensor_name': sensor_name,
                'value': value
            }

            # Serialize the message to JSON
            message_json = json.dumps(message)

            # Send the message to Kafka
            producer.produce(topic=kafka_topic, value=message_json, key=sensor_name)
            #time.sleep(0.1)

    finally:
        # Close the producer
        producer.flush()

    # Wait for a while before generating the data again
    time.sleep(1)
