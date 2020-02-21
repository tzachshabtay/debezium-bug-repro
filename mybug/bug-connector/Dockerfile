FROM debezium/connect:latest

USER root

RUN cd /tmp && \
  curl -sfSL -o /tmp/apache-maven-3.3.9-bin.tar.gz http://www-eu.apache.org/dist/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz && \
  tar xvf apache-maven-3.3.9-bin.tar.gz && \
  mv apache-maven-3.3.9 /opt/maven && \
  rm apache-maven-3.3.9-bin.tar.gz

ENV M2_HOME="/opt/maven"
ENV PATH="/opt/maven//bin:${PATH}"
ENV LOG_LEVEL=INFO

# install our custom connector
COPY . /tmp/mybug
WORKDIR /tmp/mybug/bug-connector
RUN mvn -e clean package
RUN mkdir $KAFKA_CONNECT_PLUGINS_DIR/mybug-connector
RUN mv target/*.jar $KAFKA_CONNECT_PLUGINS_DIR/mybug-connector/
RUN rm -rf /tmp/mybug/

COPY log4j.properties $KAFKA_HOME/config/log4j.properties

USER kafka
WORKDIR $KAFKA_HOME
