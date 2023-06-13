from confluent_kafka import Consumer, TopicPartition
import json

# Prompt user for inputs
kafka_broker = input("Enter Kafka broker (format - localhost:9092): ")
kafka_topic = input("Enter Kafka topic: ")
offset = input("Enter offset (for beginning, type 'beginning'. For end, type 'end'): ")

# Validate offset input
if offset.lower() not in ['beginning', 'end']:
    try:
        offset = int(offset)
    except ValueError:
        print("Invalid offset input. Please enter a valid integer, 'beginning', or 'end'.")
        exit()


# Create a Kafka consumer
consumer = Consumer({
    'bootstrap.servers': kafka_broker,
    'group.id': 'testgroup',
    'auto.offset.reset': 'earliest'
})

if offset.lower() == 'beginning':
    consumer.assign([TopicPartition(kafka_topic, 0, 0)])  # Start from the beginning
elif offset.lower() == 'end':
    consumer.assign([TopicPartition(kafka_topic, 0, consumer.get_watermark_offsets(TopicPartition(kafka_topic, 0))[1] - 1)])  # Start from the end
else:
    consumer.assign([TopicPartition(kafka_topic, 0, offset)])  # Start from user-defined offset

# Print each message
try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        print("Read msg with offset {} from Kafka: {}".format(msg.offset(), msg.value().decode('utf-8')))
except KeyboardInterrupt:
    pass
finally:
    # Close down consumer to commit final offsets.
    consumer.close()
