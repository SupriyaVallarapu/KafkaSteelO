


from flask import request, jsonify, Blueprint
import requests
import logging

RDBMSconnector_blueprint=Blueprint("RDBMSconnector_blueprint",__name__)

CONNECTOR_CLASS = "io.confluent.connect.jdbc.JdbcSourceConnector"
VALIDATE_NON_NULL = "false"
VALUE_CONVERTER = "org.apache.kafka.connect.json.JsonConverter"
KEY_CONVERTER = "org.apache.kafka.connect.json.JsonConverter"
print("abc1")
@RDBMSconnector_blueprint.route('/api/dataconnector', methods=['POST'])
def process_json():
    print("abc")
    logging.info(request.json)
    try:
        # Get the JSON from the request
        print(f"Incoming request data: {request.json}")

        data = request.json

        # Extract the specific values you're interested in
        incrementing_column_name = data.get('incrementing_column_name')
        timestamp_column_name = data.get('timestamp_column_name')
        connection_password = data.get('connection_password')
        key_converter_schemas_enable=data.get('key_converter_schemas_enable')
        topic_prefix=data.get('topic_prefix')
        connection_user=data.get('connection_user')
        value_converter_schemas_enable=data.get('value_converter_schemas_enable')
        name=data.get('name')
        connection_url=data.get('connection_url')
        table_include_list = data.get('table_include_list')
        mode = data.get('mode')

        # Check if any values are missing and return an error if they are
        if mode == "incrementing":
            if not all([incrementing_column_name, connection_password, key_converter_schemas_enable, topic_prefix, 
            connection_user, value_converter_schemas_enable, name, connection_url, table_include_list]):
                return jsonify(error='One or more required values were not provided'), 400
        elif mode == "timestamp":
            if not all([timestamp_column_name, connection_password, key_converter_schemas_enable, topic_prefix, 
            connection_user, value_converter_schemas_enable, name, connection_url, table_include_list]):
                return jsonify(error='One or more required values were not provided'), 400

        # Build the response data
        response_data = {
            'name': name,
            'config': {
                'connector.class': CONNECTOR_CLASS,
                'validate.non.null': VALIDATE_NON_NULL,
                'mode': mode,
                'key.converter.schemas.enable': key_converter_schemas_enable,
                'topic.prefix': topic_prefix,
                'connection.user': connection_user,
                'connection.password':connection_password,
                'value.converter.schemas.enable': value_converter_schemas_enable,
                'connection.url': connection_url,
                'table.whitelist': table_include_list,
                'value.converter': VALUE_CONVERTER,
                'key.converter': KEY_CONVERTER
            }
        }
        
        if mode == "incrementing":
            response_data['config']['incrementing.column.name'] = incrementing_column_name
        elif mode == "timestamp":
            response_data['config']['timestamp.column.name'] = timestamp_column_name

        print(f"Sending data to Kafka Connect: {response_data}")
        kafka_connect_response = requests.post('http://kafkasteelo-kafka-connect-1:8083/connectors', json=response_data)
        print(f"Kafka Connect response: {kafka_connect_response.status_code}, {kafka_connect_response.text}")
        if kafka_connect_response.status_code != 201:
            return jsonify(
                error='Failed to create Kafka Connect connector',
                kafka_response=kafka_connect_response.json(),
                kafka_response_status=kafka_connect_response.status_code
            ), 500

        return jsonify(success=True)
    except Exception as e:
        return jsonify(error=str(e)), 500

