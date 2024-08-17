# Use an official OpenJDK runtime as a parent image
FROM openjdk:11-jre-slim

# Set the working directory
WORKDIR /usr/local/blazegraph

# Install curl and download Blazegraph JAR
RUN apt-get update && \
    apt-get install -y curl && \
    curl -L https://github.com/blazegraph/blazegraph-python

# Expose the port Blazegraph runs on
EXPOSE 8080

# Command to run Blazegraph
ENTRYPOINT ["java", "-Xmx4g", "-jar", "blazegraph.jar"]
