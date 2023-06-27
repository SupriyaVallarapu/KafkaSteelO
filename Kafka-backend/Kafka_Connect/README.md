# Kafka Connect Custom Docker Image

This repository contains a Dockerfile and associated Kafka Connect plugins to create a custom Kafka Connect Docker image based on the Confluent Kafka Connect Base image.

## Dockerfile

The Dockerfile extends from the latest Confluent Kafka Connect Base image and copies the connector plugins from the `plugins/` directory to `/opt/kafka/plugins/` in the image. It also sets the Kafka Connect plugin path to this directory. 

You can build your Docker image using the following command:

**'docker build -f /path/to/this/Dockerfile . -t my-connector-image-name'**

Remember to replace **`/path/to/this/Dockerfile`** with the actual path to the Dockerfile.


## Plugins Folder
This repository includes the following plugins in the plugins/ directory:

1. clickhouse-kafka-connect-v0.0.10-beta
2. confluentinc-kafka-connect-mqtt-1.7.0
3. confluentinc-kafka-connect-avro-converter-7.4.0
4. confluentinc-kafka-connect-oracle-cdc-2.6.1
5. confluentinc-kafka-connect-cassandra-2.0.5
6. confluentinc-kafka-connect-s3-10.5.1
7. confluentinc-kafka-connect-ftps-1.0.5-preview
8. debezium-debezium-connector-mysql-2.2.1
9. confluentinc-kafka-connect-github-2.1.4
10. debezium-debezium-connector-postgresql-2.2.1
11. confluentinc-kafka-connect-hdfs3-source-2.5.3
12. debezium-debezium-connector-sqlserver-2.2.1
13. confluentinc-kafka-connect-http-1.7.2
14. mongodb-kafka-connect-mongodb-1.10.1
15. confluentinc-kafka-connect-influxdb-1.2.8
16. snowflakeinc-snowflake-kafka-connector-1.9.3
17. confluentinc-kafka-connect-json-schema-converter-7.4.0

## Source and Sink Properties
The 'source/' and 'sink/' directories contain JSON template files for various source and sink properties. You can use these templates to configure your Kafka Connect sources and sinks.

I hope this repository aids you in setting up and deploying your custom Kafka Connect Docker image. If you have any questions or issues, feel free to raise an issue on this repository.

