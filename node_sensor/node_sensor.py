import time
import random
import pika
from influxdb_client import InfluxDBClient
from influxdb_client import InfluxDBClient, BucketsApi
from influxdb_client.client.exceptions import InfluxDBError

# Configurações do Broker AMQP
BROKER_URL = "amqp://rabbitmq:rabbitmq@localhost:5672/"
EXCHANGE_NAME = "fm.fanout"

# Configurações do InfluxDB
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "NwM3ta7vunbyUzySwxSgNMCRhGRYoHzGNY0yPap2nKvtYGNaMcarfp5_bvtKM85vTpXcXDffcGbputShx0v6ng==" #"your-token-here"
INFLUXDB_ORG = "my-org"
BUCKET_NAME = "sensor_data"

# Parâmetros de simulação
INITIAL_NODES = 2
MAX_NODES = 16
MESSAGES_PER_NODE = 10

# Função para verificar ou criar um bucket no InfluxDB
def ensure_bucket_exists():
    try:
        with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
            buckets_api = client.buckets_api()
            
            # Verificar se o bucket já existe
            buckets = buckets_api.find_buckets().buckets
            if any(bucket.name == BUCKET_NAME for bucket in buckets):
                print(f"Bucket '{BUCKET_NAME}' já existe.")
                return
            
            # Criar o bucket se não existir
            retention_rules = None  # Configure a retenção, se necessário
            buckets_api.create_bucket(bucket_name=BUCKET_NAME, org=INFLUXDB_ORG, retention_rules=retention_rules)
            print(f"Bucket '{BUCKET_NAME}' criado com sucesso.")
    except InfluxDBError as e:
        print(f"Erro ao verificar/criar o bucket: {e}")
        exit(1)

# Função para verificar ou criar uma tag no InfluxDB
def ensure_tag_exists(node_id):
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    write_api = client.write_api()

    # Escrever a tag no InfluxDB
    data = f"node_info,node_id={node_id} value=1"
    write_api.write(bucket=BUCKET_NAME, org=INFLUXDB_ORG, record=data)
    print(f"Tag criada no InfluxDB para o node_id: {node_id}")

    client.close()

# Função para publicar mensagens no broker
def publish_data_to_broker(channel, node_id, sensor_data):
    message = {
        "node_id": node_id,
        "data": sensor_data,
        "timestamp": time.time()
    }
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key='',
        body=str(message)
    )
    print(f"Mensagem enviada: {message}")

# Função principal para simular a rede de sensores
def sensor_network_simulation():
    connection = pika.BlockingConnection(pika.URLParameters(BROKER_URL))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout', durable=True)
    #channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout') 


    current_nodes = INITIAL_NODES
    node_counters = {f"node{i}": 0 for i in range(1, current_nodes + 1)}

    for node_id in node_counters:
        ensure_tag_exists(node_id)

    while current_nodes <= MAX_NODES:
        for node_id in list(node_counters.keys()):
            if node_counters[node_id] < MESSAGES_PER_NODE:
                sensor_data = {
                    "humidity": random.uniform(30.0, 90.0),
                    "temperature": random.uniform(20.0, 35.0),
                    "river_level": random.uniform(0.5, 5.0),
                    "precipitation": random.uniform(0.0, 50.0)
                }
                publish_data_to_broker(channel, node_id, sensor_data)
                node_counters[node_id] += 1
                time.sleep(1)

        if all(count >= MESSAGES_PER_NODE for count in node_counters.values()) and current_nodes < MAX_NODES:
            current_nodes *= 2
            for i in range(len(node_counters) + 1, current_nodes + 1):
                new_node_id = f"node{i}"
                node_counters[new_node_id] = 0
                ensure_tag_exists(new_node_id)

    connection.close()

if __name__ == "__main__":
    try:
        print("Iniciando a simulação de rede de sensores...")
        
        # Verificar e criar o bucket no InfluxDB, se necessário
        ensure_bucket_exists()
        
        # Iniciar a simulação da rede de sensores
        sensor_network_simulation()
    except KeyboardInterrupt:
        print("\nSimulação interrompida pelo usuário.")
    except Exception as e:
        print(f"Erro durante a execução: {e}")