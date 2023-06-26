import time
from opcua import Client
from confluent_kafka import Producer
import json

kafka_broker = "localhost:9092"
# Get user inputs
opcua_url = input("Enter the URL of the OPCUA server (format - opc.tcp://localhost:4840): ")
node_ids = input("Enter the node IDs to subscribe to, separated by commas (format - ns=2;i=4,ns=2;i=3): ").split(',')
kafka_broker = input("Enter the Kafka broker (default - localhost:9092): ") or kafka_broker
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


def publish_to_kafka(data, display_name, timestamp, cur=None, conn=None):
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



while True:
    try:
        # Get the data from the OPCUA server and publish it to Kafka
        for node_id in node_ids:
            data, display_name, timestamp = get_opcua_data(opcua_url, node_id)
            publish_to_kafka(data, display_name, timestamp)

        # Wait for a while before polling the OPCUA server again
        time.sleep(0.1)

    except Exception as e:
        print(f"Error occurred: {e}")
        time.sleep(10)
