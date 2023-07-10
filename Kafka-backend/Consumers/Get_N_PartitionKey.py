import json
from flask import Blueprint, Flask, Response, jsonify, request
from confluent_kafka import Consumer, TopicPartition
from functools import wraps

get_n_partitionkey_blueprint = Blueprint('get_n_partitionkey_blueprint', __name__)

# def handle_exceptions(func):
#     @wraps(func)
#     def decorated_function(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500
#     return decorated_function

# def validate_input(func):
#     @wraps(func)
#     def decorated_function(*args, **kwargs):
#         offset = kwargs.get('offset')
#         group_id = kwargs.get('group_id')
#         n = kwargs.get('n')

#         if offset not in ['earliest', 'latest']:
#             return jsonify({'error': 'Invalid offset parameter'}), 400

#         if not group_id:
#             return jsonify({'error': 'Missing group_id parameter'}), 400

#         if n <= 0:
#             return jsonify({'error': 'Invalid n parameter'}), 400

#         return func(*args, **kwargs)
#     return decorated_function

# def get_partition_id(consumer_config, topic, partition_key):
#     try:
#         consumer = Consumer(consumer_config)
#         partitions = consumer.list_topics(topic).topics[topic].partitions.keys()
#         consumer.assign([TopicPartition(topic, partition) for partition in partitions])

#         while True:
#             msg = consumer.poll(1.0)
#             if msg is None:
#                 break
#             if msg.error():
#                 print("Error: {}".format(msg.error()))
#                 continue

#             if msg.key() == partition_key.encode('utf-8'):
#                 consumer.close()
#                 return msg.partition()

#     except Exception as e:
#         raise Exception(f"Error while getting partition information: {str(e)}")

#     return None

# def consume_messages_partition(consumer_config, topic, partition_id, partition_key, n):
#     consumer = Consumer(consumer_config)
#     consumer.assign([TopicPartition(topic, partition_id)])

#     messages = []

#     while True:
#         msg = consumer.poll(5.0)
#         if msg is None:
#             break
#         if msg.error():
#             print("Error: {}".format(msg.error()))
#             continue

#         message_key = msg.key().decode('utf-8')
#         if message_key == partition_key:
#             message_value = msg.value().decode('utf-8')
#             messages.append(json.loads(message_value))

#             if len(messages) >= n:
#                 break

#     consumer.close()

#     return messages

# def consume_messages_n(consumer, topic, n):
#     messages = []

#     # Get the number of partitions for the topic
#     partitions = list(consumer.list_topics(topic).topics[topic].partitions.keys())
#     num_partitions = len(partitions)

#     if num_partitions == 1:
#         # If there's only one partition, all messages come from the same partition
#         tp = TopicPartition(topic, partitions[0])
#         consumer.assign([tp])
#         remaining_messages = n

#         while remaining_messages > 0:
#             msg = consumer.poll(1.0)
#             if msg is None:
#                 break
#             if msg.error():
#                 print("Error: {}".format(msg.error()))
#                 continue

#             message_value = msg.value().decode('utf-8')
#             messages.append(json.loads(message_value))
#             remaining_messages -= 1

#     else:
#         messages_per_partition = n // num_partitions
#         remaining_messages = n % num_partitions

#         for partition in partitions:
#             tp = TopicPartition(topic, partition)
#             consumer.assign([tp])
#             num_messages = messages_per_partition

#             if remaining_messages > 0:
#                 num_messages += 1
#                 remaining_messages -= 1

#             while num_messages > 0:
#                 msg = consumer.poll(1.0)
#                 if msg is None:
#                     break
#                 if msg.error():
#                     print("Error: {}".format(msg.error()))
#                     continue

#                 message_value = msg.value().decode('utf-8')
#                 messages.append(json.loads(message_value))
#                 num_messages -= 1

#     return messages

# @get_n_partitionkey_blueprint.route('/get/<offset>/<topic>/<group_id>/<int:n>', methods=['GET'])
# @get_n_partitionkey_blueprint.route('/get/<offset>/<topic>/<group_id>/<int:n>', methods=['GET'], defaults={'partition_key': ''})
# @handle_exceptions
# @validate_input
# def get_partition_and_messages(offset, topic, group_id, n, partition_key):
#     partition_key = request.args.get('partition_key')

#     consumer_config = {
#         'bootstrap.servers': 'kafka1:19092',
#         'group.id': group_id,
#         'auto.offset.reset': offset,
#         'enable.auto.commit': False
#     }

#     if partition_key:
#         partition_id = get_partition_id(consumer_config, topic, partition_key)
#         if partition_id is None:
#             return jsonify({'error': 'Partition ID not found'}), 404

#         messages = consume_messages_partition(consumer_config, topic, partition_id, partition_key, n)
#     else:
#         consumer = Consumer(consumer_config)
#         messages = consume_messages_n(consumer, topic, n)
#         consumer.close()

#     return jsonify(messages)

# # if __name__ == '__main__':
# #     app.run(port=3002)

def consume_messages_partition(consumer_config, topic, partition_id, partition_key, n):
    consumer = Consumer(consumer_config)
    consumer.assign([TopicPartition(topic, partition_id)])

    messages_sent = 0
    while messages_sent < n:
        msg = consumer.poll(5.0)
        if msg is None:
            continue
        if msg.error():
            print("Error: {}".format(msg.error()))
            continue

        message_key = msg.key().decode('utf-8')
        if message_key == partition_key:
            message_value = msg.value().decode('utf-8')
            yield 'data: %s\n\n' % json.dumps(json.loads(message_value))
            messages_sent += 1

    consumer.close()

def get_partition_id(consumer_config, topic, partition_key):
    try:
        consumer = Consumer(consumer_config)
        partitions = consumer.list_topics(topic).topics[topic].partitions.keys()
        consumer.assign([TopicPartition(topic, partition) for partition in partitions])

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                break
            if msg.error():
                print("Error: {}".format(msg.error()))
                continue

            if msg.key() == partition_key.encode('utf-8'):
                consumer.close()
                return msg.partition()

    except Exception as e:
        raise Exception(f"Error while getting partition information: {str(e)}")

    return None

def consume_messages_n(consumer, topic, n):
    # Get the number of partitions for the topic
    partitions = list(consumer.list_topics(topic).topics[topic].partitions.keys())
    num_partitions = len(partitions)

    messages_sent = 0
    while messages_sent < n:
        for partition in partitions:
            tp = TopicPartition(topic, partition)
            consumer.assign([tp])

            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Error: {}".format(msg.error()))
                continue

            message_value = msg.value().decode('utf-8')
            yield 'data: %s\n\n' % json.dumps(json.loads(message_value))
            messages_sent += 1

            if messages_sent >= n:
                break

@get_n_partitionkey_blueprint.route('/get/<offset>/<topic>/<group_id>/<int:n>', methods=['GET'])
@get_n_partitionkey_blueprint.route('/get/<offset>/<topic>/<group_id>/<int:n>', methods=['GET'], defaults={'partition_key': ''})
def get_partition_and_messages(offset, topic, group_id, n, partition_key):
    partition_key = request.args.get('partition_key')

    consumer_config = {
        'bootstrap.servers': 'kafka1:19092',
        'group.id': group_id,
        'auto.offset.reset': offset,
        'enable.auto.commit': False
    }

    def generate():
        if partition_key:
            partition_id = get_partition_id(consumer_config, topic, partition_key)
            if partition_id is None:
                yield 'data: %s\n\n' % json.dumps({'error': 'Partition ID not found'})
            else:
                yield from consume_messages_partition(consumer_config, topic, partition_id, partition_key, n)
        else:
            consumer = Consumer(consumer_config)
            yield from consume_messages_n(consumer, topic, n)
            consumer.close()

    return Response(generate(), mimetype='text/event-stream')
