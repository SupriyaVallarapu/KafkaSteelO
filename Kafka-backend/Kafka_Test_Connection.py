from confluent_kafka import Producer, KafkaError

# Prompt user for inputs
kafka_broker = input("Enter Kafka broker (format - localhost:9092): ")

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

# Create a Kafka producer
producer = Producer({'bootstrap.servers': kafka_broker})

# Try to connect to the Kafka cluster
try:
    # Try to produce a dummy message to test the connection
    producer.produce('test_topic', 'test_message', callback=delivery_report)
except Exception as e:
    print("Unable to produce message to Kafka broker: {}. Please check the broker address.".format(kafka_broker))
    print("Exception: ", e)

# Wait for any outstanding messages to be delivered and delivery reports to be received.
producer.flush()

