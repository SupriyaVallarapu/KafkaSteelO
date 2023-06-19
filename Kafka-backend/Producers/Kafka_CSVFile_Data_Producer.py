# from flask import Flask, request
# from flask_cors import CORS
# import os
# import time
# import pandas as pd
# from confluent_kafka import Producer
# import json

# app = Flask(__name__)
# cors=CORS(app)

# cors = CORS(app, resources={r"/*": {"origins": ["http://localhost:8080", "http://localhost:3000"]}})

# producer = None
# processed_files = set()
# kafka_broker = None
# kafka_topic = None

# @app.route('/api/csvupload', methods=['POST'])
# def upload_csv():
#     global producer, processed_files, kafka_broker, kafka_topic

#     # Get the directory path, Kafka broker, and Kafka topic from the request
#     data_dir = request.json['data_dir']
#     new_kafka_broker = request.json['kafka_broker']
#     new_kafka_topic = request.json['kafka_topic']

#     # Create a producer if it doesn't exist or if the Kafka broker or topic has changed
#     if producer is None or new_kafka_broker != kafka_broker or new_kafka_topic != kafka_topic:
#         if producer is not None:
#             producer.flush()
#         kafka_broker = new_kafka_broker
#         kafka_topic = new_kafka_topic
#         producer = create_producer(kafka_broker, kafka_topic)

#     # Process any new files
#     files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
#     for file in files:
#         if file not in processed_files:
#             process_file(os.path.join(data_dir, file), producer)

#     return 'CSV Data uploaded to Kafka successfully!'

# def create_producer(kafka_broker, kafka_topic):
#     return Producer({
#         'bootstrap.servers': kafka_broker,
#         'queue.buffering.max.messages': 10000000,  # Set the desired queue size
#         'compression.type': 'zstd'  # Or 'snappy', 'lz4', 'zstd'
#     })

# def process_file(filepath, producer):
#     # Load the CSV file into a pandas DataFrame
#     df = pd.read_csv(filepath)

#     try:
#         for _, row in df.iterrows():
#             # Convert each row to a dictionary
#             row_dict = row.to_dict()

#             # Serialize the row to JSON
#             message_json = json.dumps(row_dict)

#             # Send the message to Kafka
#             producer.produce(topic=kafka_topic, value=message_json)

#             time.sleep(0.1)
#     finally:
#         # Flush any outstanding messages
#         producer.flush()

# if __name__ == '__main__':
#     app.run(port= 8080)

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
import pandas as pd
from confluent_kafka import Producer, KafkaException
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:8080", "http://localhost:3000"]}})

@app.route('/api/csvupload', methods=['POST'])
def upload_csv():
    # Get the directory path, Kafka broker, and Kafka topic from the request
    data = request.get_json()

    # Ensure required fields are provided
    required_fields = ['data_dir', 'kafka_broker', 'kafka_topic']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields in request data'}), 400

    data_dir = data['data_dir']
    kafka_broker = data['kafka_broker']
    kafka_topic = data['kafka_topic']

    # Check if data_dir exists
    if not os.path.isdir(data_dir):
        return jsonify({'error': f'Directory {data_dir} does not exist'}), 400

    # Check if there are any CSV files in the directory
    files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    if not files:
        return jsonify({'error': f'No CSV files found in directory {data_dir}'}), 400

    # Create a Kafka producer
    try:
        producer = create_producer(kafka_broker)
    except KafkaException as e:
        return jsonify({'error': f'Unable to connect to Kafka broker at {kafka_broker}. Error: {str(e)}'}), 500

    # Process any new files
    for file in files:
        process_file(os.path.join(data_dir, file), producer, kafka_topic)

    return jsonify({'message': 'CSV Data uploaded to Kafka successfully!'}), 200

def create_producer(kafka_broker):
    return Producer({
        'bootstrap.servers': kafka_broker,
        'queue.buffering.max.messages': 10000000,
        'compression.type': 'zstd'
    })

def process_file(filepath, producer, kafka_topic):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(filepath)

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

if __name__ == '__main__':
    app.run(port=8080)
