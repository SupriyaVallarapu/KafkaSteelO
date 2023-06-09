from flask import Blueprint, Flask, jsonify
from confluent_kafka import Consumer, TopicPartition
import json

# get_latest_blueprint = Blueprint('get_latest_blueprint', __name__)

# def consume_messages_all(consumer_config, topic):
#     try:
#         consumer = Consumer(consumer_config)
#         messages = []

#         # Check if the topic exists
#         topics = consumer.list_topics().topics
#         if topic not in topics:
#             raise Exception("Topic '{}' does not exist".format(topic))

#         # Get the list of partitions for the topic
#         partitions = topics[topic].partitions.keys()
#         consumer.assign([TopicPartition(topic, partition) for partition in partitions])

#         while True:
#             msg = consumer.poll(1.0)
#             if msg is None:
#                 break
#             if msg.error():
#                 raise Exception("Kafka error: {}".format(msg.error()))

#             message = msg.value().decode('utf-8')
#             messages.append(json.loads(message))

#         consumer.close()

#         return messages
#     except Exception as e:
#         raise Exception("Failed to consume messages: {}".format(str(e)))


# @get_latest_blueprint.route('/get/<offset>/<topic>/<group_id>', methods=['GET'])
# def get_all_messages(offset, topic, group_id):
#     # Validate offset
#     offset = offset.lower()
#     if offset not in ["earliest", "latest"]:
#         return jsonify(error="Invalid offset"), 400

#     # Validate topic and group_id
#     if not topic or not group_id:
#         return jsonify(error="Invalid topic or group ID"), 400

#     # Validate group_id format (only alphanumeric characters and underscores allowed)
#     if not group_id.isalnum() or "_" in group_id:
#         return jsonify(error="Invalid group ID format. Only alphanumeric characters are allowed."), 400

#     consumer_config = {
#         'bootstrap.servers': 'kafka1:19092',
#         'group.id': group_id,
#         'auto.offset.reset': offset,
#         'enable.auto.commit': False
#     }

#     try:
#         messages = consume_messages_all(consumer_config, topic)
#         return jsonify(messages)
#     except Exception as e:
#         return jsonify(error="Failed to retrieve messages: {}".format(str(e))), 500


# # if __name__ == '__main__':
# #     app.run(port=3002)



from flask import Blueprint, Flask, Response, jsonify
from confluent_kafka import Consumer, TopicPartition
import json

get_latest_blueprint = Blueprint('get_latest_blueprint', __name__)

@get_latest_blueprint.route('/get/<offset>/<topic>/<group_id>', methods=['GET'])
def get_all_messages(offset, topic, group_id):
    # Validate offset
    offset = offset.lower()
    if offset not in ["earliest", "latest"]:
        return jsonify(error="Invalid offset"), 400

    # Validate topic and group_id
    if not topic or not group_id:
        return jsonify(error="Invalid topic or group ID"), 400

    consumer_config = {
        'bootstrap.servers': 'kafka1:19092',
        'group.id': group_id,
        'auto.offset.reset': offset,
        'enable.auto.commit': False
    }

    try:
        def generate():
            consumer = Consumer(consumer_config)

            # Check if the topic exists
            topics = consumer.list_topics().topics
            if topic not in topics:
                raise Exception("Topic '{}' does not exist".format(topic))

            # Get the list of partitions for the topic
            partitions = topics[topic].partitions.keys()
            consumer.assign([TopicPartition(topic, partition) for partition in partitions])

            no_message_count = 0
            while True:
                msg = consumer.poll(1)
                if msg is None:
                    no_message_count += 1
                    if no_message_count > 10:  # adjust the limit as needed
                        yield 'data: %s\n\n' % json.dumps({"status": "No new messages"})
                        break  # or continue, depending on the desired behavior
                elif msg.error():
                    raise Exception("Kafka error: {}".format(msg.error()))
                else:
                    no_message_count = 0
                    message = msg.value().decode('utf-8')
                    yield 'data: %s\n\n' % json.loads(message)
        
        return Response(generate(), mimetype='text/event-stream')

    except Exception as e:
        return jsonify(error="Failed to retrieve messages: {}".format(str(e))), 500


