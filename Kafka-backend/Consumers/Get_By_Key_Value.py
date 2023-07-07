from flask import Blueprint, Flask, Response, jsonify
from confluent_kafka import Consumer, TopicPartition
import json

get_by_key_value_blueprint = Blueprint('get_by_key_value_blueprint', __name__)

def consume_messages_all(consumer_config, topic):
    try:
        consumer = Consumer(consumer_config)
        messages = []

        topics = consumer.list_topics().topics
        if topic not in topics:
             error_message = "topic does not exist."
             return Response(json.dumps({"error": error_message}), status=400, mimetype='application/json')
        
        # Get the list of partitions for the topic
        partitions = consumer.list_topics(topic).topics[topic].partitions.keys()

        # Assign all partitions to the consumer
        consumer.assign([TopicPartition(topic, partition) for partition in partitions])

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                break
            if msg.error():
                error_message = "Error: {}".format(msg.error())
                consumer.close()
                return Response(json.dumps({"error": error_message}), status=500, mimetype='application/json')

            message = msg.value().decode('utf-8')
            messages.append(message)

        consumer.close()

        return messages
    except Exception as e:
        error_message = "An error occurred while consuming messages: {}".format(str(e))
        return Response(json.dumps({"error": error_message}), status=500, mimetype='application/json')


def search_messages_by_key_value(messages, key, value):
    found_messages = []

    for message in messages:
        try:
            message_dict = json.loads(message)
            if key in message_dict:
                message_value = message_dict[key]
                # Handle conversion if the value is an integer
                if isinstance(message_value, int):
                    value = int(value)
                if message_value == value:
                    found_messages.append(message_dict)
        except json.JSONDecodeError as e:
            error_message = "Invalid JSON message: {}".format(str(e))
            print(error_message)  # or log the error for debugging purposes

    return found_messages

@get_by_key_value_blueprint.route('/get/key-value/<offset>/<topic>/<group_id>/<key>/<value>', methods=['GET'])
def get_messages_by_key_value(offset, topic, group_id, key, value):
    try:
        consumer_config = {
            'bootstrap.servers': 'kafka1:19092',
            'group.id': group_id,
            'auto.offset.reset': offset,
            'enable.auto.commit': False
        }

        # Validate the offset value
        if offset not in ['earliest', 'latest']:
            error_message = "Invalid offset value. Must be 'earliest' or 'latest'."
            return Response(json.dumps({"error": error_message}), status=400, mimetype='application/json')

        messages = consume_messages_all(consumer_config, topic)
        found_messages = search_messages_by_key_value(messages, key, value)
        json_data = json.dumps(found_messages)
        return Response(json_data, mimetype='application/json')
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return Response(json.dumps({"error": error_message}), status=500, mimetype='application/json')


# if __name__ == '__main__':
#         app.run(port=3002)

