from flask import Blueprint, request, jsonify
import time
import pandas as pd
from confluent_kafka import Producer, KafkaException
import json
import threading
import os

csv_blueprint = Blueprint('csv_blueprint', __name__)

processed_files = set()

@csv_blueprint.route('/api/csvupload', methods=['POST'])
def start_process():
    data = request.get_json()

    data_dir = request.args.get('data_dir', '/app/data')
    kafka_broker = data.get('kafka_broker')
    kafka_topic = data.get('kafka_topic')

    # Check if data_dir exists
    if not os.path.isdir(data_dir):
        return jsonify({'error': f'Directory {data_dir} does not exist'}), 400

    try:
        producer = create_kafka_producer(kafka_broker)
    except KafkaException as e:
        return jsonify({'error': f'Unable to connect to Kafka broker at {kafka_broker}. Error: {str(e)}'}), 500

    # Start a new thread that will collect and stream data
    threading.Thread(target=collect_and_stream_data, args=(data_dir, kafka_topic, producer)).start()

    return jsonify({'message': 'CSV Data upload process started.'}), 200

def collect_and_stream_data(data_dir, kafka_topic, producer):
    while True:
        # Check if there are any CSV files in the directory
        files = [f for f in os.listdir(data_dir) if f.endswith('.csv') and f not in processed_files]
        if not files:
            time.sleep(10)
            continue

        # Process any new files
        for file in files:
            try:
                process_file(os.path.join(data_dir, file), kafka_topic, producer)
                processed_files.add(file)
            except Exception as e:
                print(f"Error processing file {file}: {e}")
        
        time.sleep(10)

def create_kafka_producer(broker):
    return Producer({
        'bootstrap.servers': broker,
        'enable.idempotence': True,
        'queue.buffering.max.messages': 10000000,  # Set the desired queue size
        'queue.buffering.max.ms': 0,
        'compression.type': 'zstd',  # 'gzip' Or 'snappy', 'lz4', 'zstd'
        'acks': 'all' 
    })

def process_file(filepath, kafka_topic, producer):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(filepath, encoding='ISO-8859-1')

    try:
        for _, row in df.iterrows():
            # Convert each row to a dictionary
            row_dict = row.to_dict()

            # Serialize the row to JSON
            message_json = json.dumps(row_dict)

            # Send the message to Kafka
            producer.produce(topic=kafka_topic, value=message_json)

            time.sleep(0.1)
    finally:
        # Flush any outstanding messages
        producer.flush()
