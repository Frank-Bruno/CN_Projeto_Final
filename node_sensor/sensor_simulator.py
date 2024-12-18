import os
import time
import random
import pika
from influxdb_client import InfluxDBClient
from influxdb_client.client.exceptions import InfluxDBError
import json

# Configurações dinâmicas (lidas do ambiente)
BROKER_URL = os.getenv("BROKER_URL", "amqp://admin:admin@rabbitmq:5672/")
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME", "fm.fanout")
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://influxdb-influxdb2:80")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "my-super-secret-token")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "my-org")
BUCKET_NAME = os.getenv("BUCKET_NAME", "sensor_data")
INITIAL_NODES = int(os.getenv("INITIAL_NODES", 2))
MAX_NODES = int(os.getenv("MAX_NODES", 10))
MESSAGES_PER_NODE = int(os.getenv("MESSAGES_PER_NODE", 10))


def ensure_bucket_exists():
    try:
        with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
            buckets_api = client.buckets_api()
            buckets = buckets_api.find_buckets().buckets
            if any(bucket.name == BUCKET_NAME for bucket in buckets):
                print(f"Bucket '{BUCKET_NAME}' já existe.")
                return
            buckets_api.create_bucket(bucket_name=BUCKET_NAME, org=INFLUXDB_ORG)
            print(f"Bucket '{BUCKET_NAME}' criado com sucesso.")
    except InfluxDBError as e:
        print(f"Erro ao criar o bucket: {e}")
        exit(1)


def ensure_tag_exists(node_id):
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api()
        data = f"node_info,node_id={node_id} value=1"
        write_api.write(bucket=BUCKET_NAME, org=INFLUXDB_ORG, record=data)
        print(f"Tag criada no InfluxDB para o node_id: {node_id}")


def publish_data_to_broker(channel, node_id, sensor_data):
    message = {"node_id": node_id, "data": sensor_data, "timestamp": time.time()}
    message_body = json.dumps(message).encode('utf-8')
    channel.basic_publish(exchange=EXCHANGE_NAME, routing_key='', body=message_body)
    print(f"Mensagem enviada: {message}")


def sensor_network_simulation():
    connection = pika.BlockingConnection(pika.URLParameters(BROKER_URL))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout', durable=True)

    current_nodes = INITIAL_NODES
    node_counters = {f"node{i}": 0 for i in range(1, current_nodes + 1)}

    for node_id in node_counters:
        ensure_tag_exists(node_id)

    while current_nodes <= MAX_NODES:
        for node_id in node_counters.keys():
            if node_counters[node_id] < MESSAGES_PER_NODE:
                sensor_data = {
                    "humidity": random.uniform(30.0, 90.0),
                    "temperature": random.uniform(20.0, 35.0),
                }
                publish_data_to_broker(channel, node_id, sensor_data)
                node_counters[node_id] += 1
                time.sleep(1)

        if all(v >= MESSAGES_PER_NODE for v in node_counters.values()) and current_nodes < MAX_NODES:
            current_nodes += 1
            new_node_id = f"node{current_nodes}"
            node_counters[new_node_id] = 0
            ensure_tag_exists(new_node_id)

    connection.close()


if __name__ == "__main__":
    ensure_bucket_exists()
    sensor_network_simulation()