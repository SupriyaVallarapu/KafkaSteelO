from flask import Blueprint, Flask, jsonify
from confluent_kafka import Consumer, TopicPartition
import json

# get_all_messages_blueprint = Blueprint('get_all_messages_blueprint', __name__)

# @get_all_messages_blueprint.route('/get/all/<offset>/<topic>/<group_id>', methods=['GET'])
# def get_all_messages(offset, topic, group_id):
#     # Validate offset
#     offset = offset.lower()
#     if offset not in ["earliest", "latest"]:
#         return jsonify(error="Invalid offset"), 400

#     # Validate topic and group_id
#     if not topic or not group_id:
#         return jsonify(error="Invalid topic or group ID"), 400

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
#             msg = consumer.poll(1)
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


# # if __name__ == '__main__':
# #     app.run(port=3002)



from flask import Blueprint, Flask, Response
from confluent_kafka import Consumer, TopicPartition
import json

get_all_messages_blueprint = Blueprint('get_all_messages_blueprint', __name__)

@get_all_messages_blueprint.route('/get/all/<offset>/<topic>/<group_id>', methods=['GET'])
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

            while True:
                msg = consumer.poll(1)
                if msg is None:
                    continue
                if msg.error():
                    raise Exception("Kafka error: {}".format(msg.error()))

                message = msg.value().decode('utf-8')
                yield 'data: %s\n\n' % json.loads(message)
        
        return Response(generate(), mimetype='text/event-stream')

    except Exception as e:
        return jsonify(error="Failed to retrieve messages: {}".format(str(e))), 500
