import requests
import csv
import time
from datetime import datetime

# Configurações
PROMETHEUS_URL = "http://localhost:9090/api/v1/query"
NODE_INSTANCE = "iot-cluster-worker2"#"172.18.0.5:9100"  # Altere para o endereço do node
INTERVAL = 10  # Intervalo entre coletas (em segundos)
DURATION = 60  # Duração total da coleta (em segundos)
OUTPUT_FILE = "node_metrics.csv"

# Consultas PromQL
QUERIES = {
    "cpu_usage": f'sum(rate(node_cpu_seconds_total{{node="{NODE_INSTANCE}", mode!="idle"}}[5m]))',
    "memory_usage": f'node_memory_Active_bytes{{node="{NODE_INSTANCE}"}}',
    "network_traffic": f'sum(rate(node_network_receive_bytes_total{{node="{NODE_INSTANCE}"}}[1m]) + rate(node_network_transmit_bytes_total{{instance="{NODE_INSTANCE}"}}[1m]))',
}

def query_prometheus(query):
    """Consulta o Prometheus e retorna o valor."""
    try:
        response = requests.get(PROMETHEUS_URL, params={"query": query})
        response.raise_for_status()
        data = response.json()
        if data["status"] == "success" and data["data"]["result"]:
            return float(data["data"]["result"][0]["value"][1])
    except Exception as e:
        print(f"Erro ao consultar Prometheus: {e}")
    return None

def collect_metrics():
    """Coleta métricas do Prometheus e armazena em um arquivo CSV."""
    with open(OUTPUT_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "cpu_usage", "memory_usage", "network_traffic"])
        
        end_time = time.time() + DURATION
        while time.time() < end_time:
            timestamp = datetime.now().isoformat()
            cpu_usage = query_prometheus(QUERIES["cpu_usage"])
            memory_usage = query_prometheus(QUERIES["memory_usage"])
            network_traffic = query_prometheus(QUERIES["network_traffic"])
            
            print(f"{timestamp} - CPU: {cpu_usage}, Memória: {memory_usage}, Rede: {network_traffic}")
            writer.writerow([timestamp, cpu_usage, memory_usage, network_traffic])
            
            time.sleep(INTERVAL)

# Executa a coleta de métricas
if __name__ == "__main__":
    print("Iniciando coleta de métricas...")
    collect_metrics()
    print(f"Métricas armazenadas em {OUTPUT_FILE}")
