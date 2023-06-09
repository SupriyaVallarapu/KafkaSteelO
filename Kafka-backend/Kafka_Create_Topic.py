from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException

# Prompt user for inputs
kafka_broker = input("Enter Kafka broker (format - localhost:9092): ")
kafka_topic = input("Enter new Kafka topic: ")
num_partitions = int(input("Enter number of partitions: "))
replication_factor = int(input("Enter replication factor: "))

# Create a Kafka admin client
admin_client = AdminClient({
    'bootstrap.servers': kafka_broker
})

# Create a new topic
new_topic = NewTopic(
    topic=kafka_topic,
    num_partitions=num_partitions,
    replication_factor=replication_factor
)


# Attempt to create the topic
fs = admin_client.create_topics([new_topic])

for topic, f in fs.items():
    try:
        f.result()  # The result itself is None
        print(f"Topic '{topic}' created successfully.")
    except Exception as e:
        print(f"Failed to create topic '{topic}': {e}")

# List all topics to confirm
try:
    topics = admin_client.list_topics().topics
    print("Current topics:")
    for topic in topics:
        print(f"- {topic}")
except KafkaException as e:
    print(f"Failed to list topics: {e}")
