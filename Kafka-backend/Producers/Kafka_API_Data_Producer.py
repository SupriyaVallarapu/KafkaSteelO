
import requests
import json
from flask import Blueprint, request, jsonify
from confluent_kafka import Producer, KafkaException
import threading
import time

api_blueprint = Blueprint('api_blueprint', __name__)

@api_blueprint.route('/api/apidata', methods=['POST'])
def start_process():
    data = request.get_json()

    required_fields = ['api_url', 'kafka_broker', 'kafka_topic']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields in request data'}), 400

    api_url = data['api_url']
    kafka_broker = data['kafka_broker']
    kafka_topic = data['kafka_topic']

    try:
        producer = create_producer(kafka_broker)
    except KafkaException as e:
        return jsonify({'error': f'Unable to connect to Kafka broker at {kafka_broker}. Error: {str(e)}'}), 500

    # Start a new thread that will collect and stream data
    threading.Thread(target=collect_and_stream_data, args=(api_url, kafka_topic, producer)).start()

    return jsonify({'message': 'API data upload process started.'}), 200

def collect_and_stream_data(api_url, kafka_topic, producer):
    while True:
        try:
            data = get_api_data(api_url)
            publish_to_kafka(data, kafka_topic, producer)
        except requests.exceptions.RequestException as e:
            print(f"Error during API call. Error: {str(e)}")
        except KafkaException as e:
            print(f"Error during Kafka operations. Error: {str(e)}")

        time.sleep(10)  # wait for 10 seconds before next API call

def create_producer(kafka_broker):
    return Producer({
        'bootstrap.servers': kafka_broker,
        'enable.idempotence': True,
        'queue.buffering.max.messages': 10000000,  # Set the desired queue size
        'queue.buffering.max.ms': 500,
        'compression.type': 'zstd',  # 'gzip' Or 'snappy', 'lz4', 'zstd'
        'acks': 'all' 
    })

def get_api_data(api_url):
    response = requests.get(api_url,verify=False)
    response.raise_for_status()
    return response.json()

def publish_to_kafka(data, kafka_topic, producer):
    message_json = json.dumps(data)
    producer.produce(topic=kafka_topic, value=message_json)
    producer.flush()
