import requests
import json
import random

def create_kafka_source():
    # Collect user inputs
    name = input("Enter name: ")
    user = input("Enter database user: ")
    dbname = input("Enter database name: ")
    password = input("Enter database password: ")
    hostname = input("Enter database hostname: ")
    port = input("Enter database port: ")
    default_partitions = input("Enter default partitions: ")
    key_converter_schemas_enable = input("Enable key converter schemas (true or false): ")
    topic_prefix = input("Enter topic prefix: ")
    value_converter_schemas_enable = input("Enable value converter schemas (true or false): ")
    default_replication_factor = input("Enter default replication factor: ")
    table_include_list = input("Enter table include list (comma separated): ")

    # Generate random slot name
    slot_name = "slot" + str(random.randint(1, 1000))

    # Prepare server name
    server_name = f"{hostname}:{port}/{dbname}.{user}"

    # Build config dictionary
    config_dict = {
        "name": name,
        "config": {
            "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
            "database.user": user,
            "database.dbname": dbname,
            "topic.creation.default.partitions": default_partitions,
            "slot.name": slot_name,
            "plugin.name": "pgoutput",
            "database.server.name": server_name,
            "database.password": password,
            "database.hostname": hostname,
            "database.port": port,
            "key.converter.schemas.enable": key_converter_schemas_enable,
            "topic.prefix": topic_prefix,
            "value.converter.schemas.enable": value_converter_schemas_enable,
            "topic.creation.default.replication.factor": default_replication_factor,
            "table.include.list": table_include_list,
            "value.converter": "org.apache.kafka.connect.json.JsonConverter",
            "key.converter": "org.apache.kafka.connect.json.JsonConverter"
        }
    }

    # Convert dict to JSON
    config_json = json.dumps(config_dict)

    # Define Kafka Connect URL
    kafka_connect_url = "http://localhost:8083/connectors" # Update to your Kafka Connect URL if different

    # Send POST request
    response = requests.post(kafka_connect_url, headers={"Content-Type": "application/json"}, data=config_json)

    # Check response
    if response.status_code == 201:
        print("Connector created successfully!")
    else:
        print(f"Failed to create connector. Status code: {response.status_code}")
        print(f"Response: {response.json()}")

create_kafka_source()
