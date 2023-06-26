import time
from confluent_kafka import Producer
import json
from datetime import datetime

kafka_topic = input("Enter the Kafka topic: ")

conf = {'bootstrap.servers': 'localhost:9092'}

producer = Producer(conf)

try:
    i = 0
    while True:
        data = {
            'value': i,
            'timestamp': datetime.now().isoformat()
        }
        producer.produce(kafka_topic, value=json.dumps(data))
        producer.flush()
        i += 1
        time.sleep(1)
except KeyboardInterrupt:
    pass
