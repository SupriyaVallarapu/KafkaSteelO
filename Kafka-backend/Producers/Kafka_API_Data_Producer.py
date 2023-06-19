import requests
import json
from flask import Blueprint, request, jsonify
from confluent_kafka import Producer, KafkaException

api_blueprint = Blueprint('api_blueprint', __name__)

@api_blueprint.route('/api/apidata', methods=['POST'])
def api_data():
    global producer, kafka_broker, kafka_topic

    # Get the directory path, Kafka broker, and Kafka topic from the request
    data = request.get_json()

    # Ensure required fields are provided
    required_fields = ['api_url', 'kafka_broker', 'kafka_topic']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields in request data'}), 400

    api_url = data['api_url']
    kafka_broker = data['kafka_broker']
    kafka_topic = data['kafka_topic']

    # Create a producer if it doesn't exist or if the Kafka broker or topic has changed
    
    try:
        producer = create_producer(kafka_broker, kafka_topic)
    except KafkaException as e:
        return jsonify({'error': f'Unable to connect to Kafka broker at {kafka_broker}. Error: {str(e)}'}), 500

    try:
        data = get_api_data(api_url)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error during API call. Error: {str(e)}'}), 500

    try:
        publish_to_kafka(data,producer)
    except KafkaException as e:
        return jsonify({'error': f'Error during Kafka operations. Error: {str(e)}'}), 500

    return jsonify({'message': 'API Data uploaded to Kafka successfully!'}), 200

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
