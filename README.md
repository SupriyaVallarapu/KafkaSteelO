# KafkaIO

# Description
KafkaIO is a service that provides a complete and user-friendly interface to interact with and manage Kafka data streaming in various contexts

# Overview

KafkaIO provides a React-based front end, enabling users to connect a broad array of data sources and publish data to Kafka topics. The service comes with a Kafka Connect component, a Schema Registry, and several API endpoints. It also provides an option to persist data to Timescale DB and includes a Kafka UI for managing the Kafka cluster, topics, consumers, and messages. KafkaIO is built on Python and React and can be deployed using Docker for proof of concept (POC).

# Data Sources (Producers)
KafkaIO allows users to connect and publish data from a variety of data sources to Kafka topics. These data sources essentially act as producers, feeding data into the Kafka ecosystem.

## CSV Files
CSV, or Comma-Separated Values, files are widely used for storing tabular data, such as a spreadsheet or database. KafkaIO can ingest data directly from CSV files, providing a simple way to input structured data.

Given a path to a directory, the producer will read every CSV file in the directory and publish the data in the file to the specified Kafka Topic in JSON format. The producer will wait for 10 seconds before scanning the directory again for new CSV files.

## Parquet Files
Parquet is a columnar storage file format optimized for use with big data processing frameworks. Its columnar nature allows for efficient compression and encoding schemes. KafkaIO's ability to read from Parquet files means it can handle complex, large-scale data efficiently.

## OPCUA
OPC Unified Architecture (OPCUA) is a machine-to-machine communication protocol for industrial automation. KafkaIO can connect directly to OPCUA systems, further enhancing its applicability in industrial contexts where this protocol is commonly used, such as the Steel industry.

## Relational Databases
Relational Databases are a crucial data source that KafkaIO can connect to. These databases, which include popular systems like MSSQL, PostgreSQL, and Oracle, store data in a structured format across multiple tables with relations.

## Kafka Connect (RDBMS Producer)
KafkaIO includes Kafka Connect, which is specifically designed to connect to Relational Database Management System (RDBMS) sources and publish data to Kafka topics using Kafka Connect configuration and plugins. This feature ensures seamless data transfer from traditional databases into the Kafka ecosystem.

# API Endpoints (Consumers)
KafkaIO provides several API endpoints that allow users to access and consume data from Kafka topics. These endpoints return data in a JSON format, making it easy to integrate and use in various applications. Here are the provided endpoints:

- Get ALL
The Get ALL endpoint retrieves all messages from a specified Kafka topic. This allows users to access all data stored in the topic, providing a comprehensive view of the information.

- Get by Key Value Pairs
This endpoint allows users to query messages based on specific key-value pairs. This feature is useful when you want to filter out data based on certain criteria or identifiers.

- Get by Key and Timestamp
With this endpoint, users can retrieve messages based on a specific key and a timestamp. This allows for the retrieval of messages that were published at a certain time and tagged with a specific key, enabling precise data access.

- Get by PartitionID
This endpoint retrieves messages from a specific partition of a Kafka topic. This is useful in cases where data is segregated into partitions for efficiency and organization purposes.

- Get by Timestamp
The Get by Timestamp endpoint retrieves messages published within a specific time range. This is particularly useful when analyzing data trends over time or recovering data from a specific operational period.

- Get Latest
The Get Latest endpoint fetches the most recent unread messages from a Kafka topic. This allows users to always have access to the latest data without having to retrieve all messages.

- Get from Multiple Partitions
This endpoint retrieves messages from multiple specified partitions of a Kafka topic. It's beneficial when working with data segregated across different partitions.

- Get Payload and Get Schema
In the context of Relational data, when messages are published with a schema and payload, these two endpoints come into play:

- The Get Payload endpoint retrieves the data itself from the topic.

- The Get Schema endpoint fetches the most recent schema from the most recent message. This ensures that users always have up-to-date schema information for the data they are consuming.

- Get PartitionID from Key
The Get PartitionID from Key endpoint returns the PartitionID for a given key. This allows users to determine which partition a certain piece of data resides in based on its key.

- Get Number of Partitions
The Get Number of Partitions endpoint returns the total number of partitions in a Kafka topic. This is useful for understanding the structure and distribution of data within a topic.


# Persist data in Timescale DB
KafkaIO offers the option to persist data to Timescale DB. This feature allows users to store their data in a database for long-term storage or further analysis. For the Steel industry, this means the ability to retain and revisit data, enabling historical analysis, trend detection, and long-term strategic planning.

# Deployment
The underlying Kafka deployment is a 3-node cluster. For POC, deployment can be done using Docker on a local machine.


# USAGE
- Run Python main.py in the backend and the OPCUA Data simulator if working with OPCUA Data, Other relational database Data simulator to stream data continuously
- Go to Kafka-fronend and run npm start to start the application
