from flask import Blueprint, request, jsonify
import time
from opcua import Client
from confluent_kafka import Producer
import json
import threading
opcua_blueprint = Blueprint('opcua_blueprint', __name__)

kafka_broker_default = "localhost:9092"

@opcua_blueprint.route('/api/opcuaproduce', methods=['POST'])
def start_process():
    data = request.get_json()

    opcua_url = data.get('opcua_url')
    node_ids = data.get('node_ids').split(',')
    kafka_broker = data.get('kafka_broker') or kafka_broker_default
    kafka_topic = data.get('kafka_topic')

    producer = create_kafka_producer(kafka_broker)

    # Start a new thread that will collect and stream data
    threading.Thread(target=collect_and_stream_data, args=(opcua_url, node_ids, kafka_topic, producer)).start()

    return {'message': 'Data collection and streaming process started.'}

def collect_and_stream_data(opcua_url, node_ids, kafka_topic, producer):
    while True:
        try:
            # Get the data from the OPCUA server and publish it to Kafka
            for node_id in node_ids:
                data, display_name, timestamp = get_opcua_data(opcua_url, node_id)
                publish_to_kafka(data, display_name, timestamp, kafka_topic, producer)

            # Wait for a while before polling the OPCUA server again
            time.sleep(0.1)

        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(10)

def create_kafka_producer(broker):
    return Producer({
        'bootstrap.servers': broker,
        'enable.idempotence': True,
        'queue.buffering.max.messages': 10000000,  # Set the desired queue size
        'queue.buffering.max.ms': 500,
        'compression.type': 'zstd',  # 'gzip' Or 'snappy', 'lz4', 'zstd'
        'acks': 'all'  # or '0' or '1' or '-1'/ 'all'
    })

def get_opcua_data(opcua_url, node_id):
    client = Client(opcua_url)
    client.connect()

    try:
        node = client.get_node(node_id)
        data_value = node.get_data_value()
        timestamp = data_value.SourceTimestamp  # get timestamp
        return node.get_value(), node.get_display_name().Text, timestamp.isoformat()
    finally:
        client.disconnect()

def publish_to_kafka(data, display_name, timestamp, kafka_topic, producer,cur=None, conn=None):
    # Create a message to be sent to Kafka
    message = {
        'sensor_name': display_name,
        'value': data,
        'timestamp': timestamp
    }

    # Convert the message to a JSON string
    message_json = json.dumps(message)

    # Send the message to Kafka
    producer.produce(topic=kafka_topic, value=message_json, key=display_name)

    # Flush the producer
    producer.flush()
