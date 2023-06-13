from confluent_kafka.admin import AdminClient

# Prompt user for Kafka broker input
kafka_broker = input("Enter Kafka broker (format - localhost:9092): ")

# Create a Kafka admin client
admin_client = AdminClient({
    'bootstrap.servers': kafka_broker
})

# Get the list of topics from the Kafka broker
topics = admin_client.list_topics().topics

# Print each topic
for topic in topics:
    print(topic)

