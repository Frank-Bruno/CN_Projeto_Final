from influxdb_client import InfluxDBClient, BucketsApi, WriteApi
from influxdb_client.client.write_api import SYNCHRONOUS

# Configurações do InfluxDB
url = "http://localhost:8086"
token = "tag" 
org = "my-org"  # Nome da organização
bucket_name = "fixed-bucket"  # Nome fixo do bucket

def create_bucket_with_tag(bucket_name, tag_key, tag_value):
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
        else:
            # Criar um novo bucket
            bucket = buckets_api.create_bucket(bucket_name=bucket_name, org_id=org_id)
            print(f"Bucket '{bucket.name}' criado com sucesso!")

        # Criar uma tag dentro do bucket
        write_api = client.write_api(write_options=SYNCHRONOUS)
        data = f"example_measurement,{tag_key}={tag_value} value=1"
        write_api.write(bucket=bucket_name, org=org, record=data)
        print(f"Tag '{tag_key}={tag_value}' adicionada ao bucket '{bucket_name}'.")

    except Exception as e:
        print(f"Erro ao criar o bucket ou adicionar a tag: {e}")
    finally:
        client.close()

# Exemplo de uso
if __name__ == "__main__":
    tag_key = "example_tag"
    tag_value = "example_value"
    create_bucket_with_tag(bucket_name, tag_key, tag_value)
