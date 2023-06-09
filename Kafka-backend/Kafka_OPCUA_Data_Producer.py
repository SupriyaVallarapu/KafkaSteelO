import time
from opcua import Client
from confluent_kafka import Producer
import psycopg2
import getpass

# Get user inputs
opcua_url = input("Enter the URL of the OPCUA server (format - opc.tcp://localhost:4840): ")
publishing_interval = int(input("Enter the frequency in seconds at which data is published by the OPCUA server: "))
node_ids = input("Enter the node IDs to subscribe to, separated by commas (format - ns=2;i=4,ns=2;i=3): ").split(',')
kafka_broker = input("Enter the Kafka broker (format - localhost:9092): ")
kafka_topic = input("Enter the Kafka topic: ")
persist_data = input("Do you want to persist the data to TimescaleDB? (yes/no): ")

# Database variables
if persist_data.lower() == 'yes':
    db_name = input("Enter your database name: ")
    db_user = input("Enter your database username: ")
    db_password = getpass.getpass("Enter your database password: ")
    db_host = input("Enter your database host (default is localhost): ")
    db_port = input("Enter your database port (default is 5432): ")

# Create a producer to send data to Kafka
producer = Producer({
    'bootstrap.servers': kafka_broker,
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
        return node.get_value(), node.get_display_name().Text
    finally:
        client.disconnect()

def publish_to_kafka(data, display_name, cur=None, conn=None):
    # Send the data to Kafka
    producer.produce(topic=kafka_topic, value=str(data))

    # Persist the data to TimescaleDB
    if conn:
        cur.execute(
            f"INSERT INTO kafkadata.{kafka_topic} (sensor_name, value) VALUES (%s, %s)",
            (display_name, data)
        )
        conn.commit()

    # Flush the producer
    producer.flush()

while True:
    conn = None
    cur = None
    try:
        # Create a connection to the database if user chose to persist data
        if persist_data.lower() == 'yes':
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )

            cur = conn.cursor()
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS kafkadata.{kafka_topic} (
                    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    sensor_name TEXT,
                    value TEXT
                );
            """)
            conn.commit()

        # Get the data from the OPCUA server and publish it to Kafka
        for node_id in node_ids:
            data, display_name = get_opcua_data(opcua_url, node_id)
            publish_to_kafka(data, display_name, cur, conn)

        # Wait for a while before polling the OPCUA server again
        time.sleep(publishing_interval)

    except Exception as e:
        print(f"Error occurred: {e}")
        if conn:
            conn.close()
        time.sleep(10)
