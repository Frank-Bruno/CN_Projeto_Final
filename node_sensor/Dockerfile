# Usando a imagem base do Python 3.9 slim
FROM python:3.9-slim

# Definindo o diretório de trabalho no contêiner
WORKDIR /app

# Copiar os arquivos da aplicação para o contêiner
COPY node_sensor.py /app/

# Instalar as dependências do Python
RUN pip install --no-cache-dir pika influxdb-client

# Expôr a porta que o aplicativo usará (se necessário)
EXPOSE 8086
EXPOSE 15672
EXPOSE 5672
# Comando para rodar o script
CMD ["python", "/app/node_sensor.py"]
