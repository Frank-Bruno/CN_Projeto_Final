from influxdb_client import InfluxDBClient, BucketsApi

# Configurações do InfluxDB
url = "http://localhost:8086"
token = "tag"
org = "my-org"  # Nome da organização

def create_bucket(bucket_name):
    try:
        # Conectar ao cliente do InfluxDB
        client = InfluxDBClient(url=url, token=token, org=org)
        buckets_api = client.buckets_api()
        orgs_api = client.organizations_api()

        # Obter o ID da organização
        orgs = orgs_api.find_organizations()
        org_id = next((organization.id for organization in orgs if organization.name == org), None)

        if not org_id:
            raise ValueError(f"Organização '{org}' não encontrada.")

        # Verificar se o bucket já existe
        existing_buckets = buckets_api.find_buckets().buckets
        if any(bucket.name == bucket_name for bucket in existing_buckets):
            print(f"Bucket '{bucket_name}' já existe.")
            return

        # Criar um novo bucket
        bucket = buckets_api.create_bucket(bucket_name=bucket_name, org_id=org_id)
        print(f"Bucket '{bucket.name}' criado com sucesso!")
    
    except Exception as e:
        print(f"Erro ao criar o bucket: {e}")
    finally:
        client.close()

# Exemplo de uso
if __name__ == "__main__":
    bucket_name = "new-bucket"
    create_bucket(bucket_name)
