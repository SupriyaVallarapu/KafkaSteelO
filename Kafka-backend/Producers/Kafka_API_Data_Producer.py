import time
from confluent_kafka import Producer
import requests
import json
from flask import Flask,Blueprint, request
from flask_cors import CORS,cross_origin

# app = Flask(__name__)
# cors = CORS(app)
# cors = CORS(app, resources={r"/*": {"origins": ["http://localhost:8080", "http://localhost:3000"]}})
api_blueprint = Blueprint('api_blueprint', __name__)


producer = None
kafka_broker = None
kafka_topic = None


@api_blueprint.route('/api/apidata', methods=['POST'])

def api_data():
    global producer, kafka_broker, kafka_topic

    # Get the directory path, Kafka broker, and Kafka topic from the request
    api_url = request.json['api_url']
    new_kafka_broker = request.json['kafka_broker']
    new_kafka_topic = request.json['kafka_topic']

    # Create a producer if it doesn't exist or if the Kafka broker or topic has changed
    if producer is None or new_kafka_broker != kafka_broker or new_kafka_topic != kafka_topic:
        if producer is not None:
            producer.flush()
        kafka_broker = new_kafka_broker
        kafka_topic = new_kafka_topic
        producer = create_producer(kafka_broker, kafka_topic)

    data = get_api_data(api_url)
    publish_to_kafka(data,producer)

    return {"status":"success"},200


def create_producer(kafka_broker, kafka_topic):
    return Producer({
        'bootstrap.servers': kafka_broker,
        'queue.buffering.max.messages': 10000000,  # Set the desired queue size
        'queue.buffering.max.ms': 500,
        'compression.type': 'zstd',  # 'gzip' Or 'snappy', 'lz4', 'zstd'
        'acks': 'all'  # or '0' or '1' or '-1'/ 'all'
    })


def get_api_data(api_url):
    response = requests.get(api_url,verify=False)

    # Raise an error if the request was unsuccessful
    response.raise_for_status()

    return response.json()


def publish_to_kafka(data,producer):
    # Serialize the message to JSON
    message_json = json.dumps(data)

    # Send the message to Kafka
    producer.produce(topic=kafka_topic, value=message_json)

    # Flush the producer
    producer.flush()

# if __name__=='__main__':
#     app.run(port=8080)


# # Get user inputs
# api_url = input("Enter the URL of the API: ")
# kafka_broker = input("Enter the Kafka broker (format - localhost:9092): ")
# kafka_topic = input("Enter the Kafka topic: ")

# # Create a producer to send data to Kafka
# producer = Producer({
#     'bootstrap.servers': kafka_broker,
#     'queue.buffering.max.messages': 10000000,  # Set the desired queue size
#     'queue.buffering.max.ms': 500,
#     'compression.type': 'zstd',  # 'gzip' Or 'snappy', 'lz4', 'zstd'
#     'acks': 'all'  # or '0' or '1' or '-1'/ 'all'
# })


# while True:
#     # Get the data from the API
#     data = get_api_data(api_url)

#     # Publish the data to Kafka
#     publish_to_kafka(data)

#     # Wait for a while before polling the API again
#     time.sleep(10)

