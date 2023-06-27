FROM confluentinc/cp-kafka-connect-base:latest

USER root:root

# Copy your connector plugins to the proper directory
COPY ./plugins/ /opt/kafka/plugins/

# Set the Kafka Connect plugin path
ENV CONNECT_PLUGIN_PATH="/opt/kafka/plugins"

# Change user back to the default user
USER 1001

# docker build -f /path/to/this/Dockerfile . -t my-connector-image-name .