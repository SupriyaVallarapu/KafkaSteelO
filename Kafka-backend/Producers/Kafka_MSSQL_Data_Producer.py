# from flask import Flask, request, jsonify,Blueprint
# import requests
# import logging

# DB_TYPE_PATHS = {
#     'postgres': '/connectors',
#     'mssql': '/mssql',
#     # Add more mappings here as needed
# }
# db_connector_blueprint=Blueprint("db_connector_blueprint",__name__)

# CONNECTOR_CLASS = "io.confluent.connect.jdbc.JdbcSourceConnector"
# VALIDATE_NON_NULL = "false"
# MODE = "incrementing"
# VALUE_CONVERTER = "org.apache.kafka.connect.json.JsonConverter"
# KEY_CONVERTER = "org.apache.kafka.connect.json.JsonConverter"

# @db_connector_blueprint.route('/api/<db_type>connector', methods=['POST'])
# def process_json(db_type):
#     logging.info(request.json) 
#     try:
#         # Get the JSON from the request
#         print(f"Incoming request data: {request.json}")

        
#         db_type_path = DB_TYPE_PATHS.get(db_type)
#         if not db_type_path:
#             return jsonify(error='Invalid db_type provided'), 400


#         data = request.json

#         # Extract the specific values you're interested in
#         incrementing_column_name = data.get('incrementing_column_name')
#         connection_password = data.get('connection_password')
#         key_converter_schemas_enable=data.get('key_converter_schemas_enable')
#         topic_prefix=data.get('topic_prefix')
#         connection_user=data.get('connection_user')
#         value_converter_schemas_enable=data.get('value_converter_schemas_enable')
#         name=data.get('name')
#         connection_url=data.get('connection_url')
#         table_include_list = data.get('table_include_list')


#         # Check if any values are missing and return an error if they are
        
#         if not all([incrementing_column_name, connection_password, key_converter_schemas_enable, topic_prefix, 
#             connection_user, value_converter_schemas_enable, name, connection_url, table_include_list]):
#             return jsonify(error='One or more required values were not provided'), 400

#         # Build the response data
#         response_data = {
#             'name': name,
#             'config': {
#                 'connector.class': CONNECTOR_CLASS,
#                 'incrementing.column.name': incrementing_column_name,
#                 'connection.password': connection_password,
#                 'validate.non.null': VALIDATE_NON_NULL,
#                 'mode': MODE,
#                 'key.converter.schemas.enable': key_converter_schemas_enable,
#                 'topic.prefix': topic_prefix,
#                 'connection.user': connection_user,
#                 'value.converter.schemas.enable': value_converter_schemas_enable,
#                 'connection.url': connection_url,
#                 'table.include.list': table_include_list,
#                 'value.converter': VALUE_CONVERTER,
#                 'key.converter': KEY_CONVERTER
#             }
#         }
#         print(f"Sending data to Kafka Connect: {response_data}")
#         kafka_connect_response = requests.post('http://localhost:8083/connectors', json=response_data)
#         print(f"Kafka Connect response: {kafka_connect_response.status_code}, {kafka_connect_response.text}")
#         if kafka_connect_response.status_code != 201:
#             return jsonify(
#                 error='Failed to create Kafka Connect connector',
#                 kafka_response=kafka_connect_response.json(),
#                 kafka_response_status=kafka_connect_response.status_code
#             ), 500

#         return jsonify(success=True)
#     except Exception as e:
#         # Return an error if something unexpected happened
#         return jsonify(error=str(e)), 500
