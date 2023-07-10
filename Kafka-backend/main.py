import threading
import os
from flask import Flask
from flask_cors import CORS
from Producers.Kafka_CSVFile_Data_Producer import csv_blueprint
from Producers.Kafka_API_Data_Producer import api_blueprint
from Producers.Kafka_ParquetFile_Data_Producer import parquet_blueprint
from Database_Persist_only.Kafka_Database_Persist_Consumer import persist_blueprint
from Producers.Kafka_OPCUA_Data_Producer import opcua_blueprint
from Database_Persist_only.Kafka_OPCUA_Database_Persist_Consumer import OPCUA_persist_blueprint
from Producers.Kafka_Data_Connect_Producer import postgres_blueprint
from Consumers.Get_All import get_all_messages_blueprint
from Consumers.Get_By_Key_Value import get_by_key_value_blueprint
from Consumers.Get_By_Name_And_Timestamps import get_by_name_and_timestamps_blueprint
from Consumers.Get_By_Timestamps import get_by_timestamp_blueprint
from Consumers.Get_Latest import get_latest_blueprint
from Consumers.Get_N_PartitionKey import get_n_partitionkey_blueprint
from Consumers.Get_PartitionId_From_PartitionKey import get_partitionid_from_partitionkey_blueprint
from Consumers.Get_Partitions import get_partitions_blueprint
from Consumers.Get_Payload import get_payload_blueprint
from Consumers.Get_Schema import get_schema_blueprint
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:8080", "http://localhost:3000","http://localhost:8083","http://localhost:3004"]}})

app.register_blueprint(csv_blueprint)
app.register_blueprint(api_blueprint)
app.register_blueprint(parquet_blueprint)
app.register_blueprint(persist_blueprint)
app.register_blueprint(opcua_blueprint)
app.register_blueprint(OPCUA_persist_blueprint)
app.register_blueprint(postgres_blueprint)
app.register_blueprint(get_all_messages_blueprint)
app.register_blueprint(get_by_key_value_blueprint)
app.register_blueprint(get_by_name_and_timestamps_blueprint)
app.register_blueprint(get_by_timestamp_blueprint)
app.register_blueprint(get_n_partitionkey_blueprint)
app.register_blueprint(get_latest_blueprint)
app.register_blueprint(get_partitionid_from_partitionkey_blueprint)
app.register_blueprint(get_partitions_blueprint)
app.register_blueprint(get_payload_blueprint)
app.register_blueprint(get_schema_blueprint)

if __name__ == "__main__":
    app.run(port=8080)


 
