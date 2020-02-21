package io.mybug.mytest.connector;

import io.confluent.connect.avro.AvroConverterConfig;
import io.confluent.connect.avro.AvroData;
import io.confluent.connect.avro.AvroDataConfig;
import io.confluent.kafka.schemaregistry.client.CachedSchemaRegistryClient;
import io.confluent.kafka.schemaregistry.client.SchemaRegistryClient;
import io.confluent.kafka.schemaregistry.client.rest.exceptions.RestClientException;
import io.confluent.kafka.serializers.AbstractKafkaAvroSerializer;
import org.apache.avro.generic.GenericRecord;
import org.apache.avro.io.Decoder;
import org.apache.avro.io.DecoderFactory;
import org.apache.avro.specific.SpecificDatumReader;
import org.apache.kafka.common.errors.SerializationException;
import org.apache.kafka.connect.data.Schema;
import org.apache.kafka.connect.data.SchemaAndValue;
import org.apache.kafka.connect.data.Struct;
import org.apache.kafka.connect.errors.DataException;
import org.apache.kafka.connect.storage.Converter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.Map;

import static org.apache.kafka.connect.transforms.util.Requirements.requireStruct;

public class BuggyConverter implements Converter {
    private final Logger logger = LoggerFactory.getLogger(getClass());

    public BuggyConverter() {
    }

    public BuggyConverter(SchemaRegistryClient client) {
    }

    public void configure(Map<String, ?> configs, boolean isKey) {
    }

    public byte[] fromConnectData(String topic, Schema schema, Object record) {
        final Struct value = requireStruct(record, "lookup");
        long id = value.getInt64("id");
        logger.info("BuggyConverter fromConnectData: {}, {}, {}", id, topic, record.getClass().getName());
        if (id == 5000) {
            throw new RuntimeException(String.format("crashing on purpose on id %s", id));
        }
        if (id > 5000) {
            throw new RuntimeException(String.format("bug reproduced! we're on id %s", id));
        }
        return new byte[5];
    }

    public SchemaAndValue toConnectData(String topic, byte[] value) {
        throw new RuntimeException("converter only supports serialization");
    }
}

