import subprocess
import psycopg2
import requests

def wait_for(url):
  print(f'waiting for {url}')
  subprocess.run(['/bin/sh', '-c', f'waitforit -timeout 100000 -address {url}'], check=True)
  print(f'{url} available')

def setup_postgres():
  wait_for('postgres:5432')
  conn = psycopg2.connect(dbname="test", user="test", password="test", host="postgres", port=5432)
  cur = conn.cursor()
  cur.execute("CREATE SCHEMA mybug;")
  cur.execute("SET search_path TO pg_catalog,public,mybug;")
  cur.execute("CREATE TABLE mybug.events (id bigserial NOT NULL,created_at timestamptz NOT NULL DEFAULT NOW(),schema_id int4 NOT NULL,data bytea NOT NULL,CONSTRAINT events_pk PRIMARY KEY (id));")
  conn.commit()
  cur.close()
  conn.close()

def setup_connector():
  wait_for('schemaregistry:8081')
  wait_for('connector:8083')
  regUrl = 'http://schemaregistry:8081'

  obj = {
      "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
      "database.hostname": "postgres",
      "database.port": 5432,
      "database.user": "test",
      "database.password": "test",
      "database.dbname": "test",
      "database.server.name": "test",

      "plugin.name": "wal2json_rds_streaming",
      "schema.refresh.mode": "columns_diff_exclude_unchanged_toast",

      "key.converter": "io.confluent.connect.avro.AvroConverter",
      "key.converter.schema.registry.url": regUrl,
      "value.converter": "io.mybug.mytest.connector.BuggyConverter",
      "value.converter.schema.registry.url": regUrl,

      "transforms": "unwrap",
      "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
      "transforms.unwrap.drop.tombstones": True,

      "table.whitelist": ".*(events|exceptions)$",
      "header.converter": "org.apache.kafka.connect.storage.SimpleHeaderConverter",
      "schema.registry.url": regUrl,
      "snapshot.delay.ms": 2000,
  }

  res = requests.put(url='http://connector:8083/connectors/micro-connector/config', json=obj)
  print(f'connector response: {res.status_code}')
  if res.status_code != 200 and res.status_code != 409 and res.status_code != 201:
      print(f'connector response text: {res.text}')
      exit(-1)

def add_events():
  conn = psycopg2.connect(dbname="test", user="test", password="test", host="postgres", port=5432)
  cur = conn.cursor()
  bin_data = b'bytes object'
  for _ in range(100000):
    cur.execute("INSERT INTO mybug.events (schema_id,data) values(%s,%s);", (1, bin_data))
  conn.commit()
  cur.close()
  conn.close()

if __name__ == '__main__':
  print("Starting setup")
  setup_postgres()
  setup_connector()
  add_events()
  print("Done adding events")