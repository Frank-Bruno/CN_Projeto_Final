"""
MQTT subscriber - Listen to a topic and sends data to InfluxDB
"""

import os
from influxdb_client import InfluxDBClient, Point
import struct
import json
import pika, sys, os
import pika.credentials

# Configuração do InfluxDB
BUCKET = "my-bucket"  # Nome do BUCKET no InfluxDB
ORG = "my-org"  # Nome da organização no InfluxDB
TOKEN ="my-super-secret-token"  # Token de acesso do InfluxDB
URL = "http://influxdb-influxdb2:8086"  # URL do servidor InfluxDB

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api()

# AMQP broker config
AMQP_BROKER_URL    = "rabbitmq-headless" 


def on_message(msg):
    """ The callback for when a PUBLISH message is received from the server."""
    # Decodifica o payload de bytes para string
    payload_str = msg.decode('utf-8')
    #test = json.dumps(payload_str)
    values = json.loads(payload_str)

    #print(type(values))
    #print(values)

    ## InfluxDB logic
    point = (
        Point(BUCKET)
        .tag("node_id", values["node_id"])
        .field("humidity", values["humidity"])
        .field("temperature", values["temperature"])
        .field("timestamp", values["timestamp"])
    )
    write_api.write(bucket=BUCKET, record=point)

def main():
    cred = pika.credentials.PlainCredentials("admin","admin")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=AMQP_BROKER_URL,credentials=cred))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        on_message(body)

    channel.basic_consume(queue='c', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
