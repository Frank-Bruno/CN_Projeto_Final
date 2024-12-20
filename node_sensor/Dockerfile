FROM python:3.9-slim

WORKDIR /app

COPY sensor_simulator_v2.py .

RUN pip install --no-cache-dir pika influxdb-client jsonschema

CMD ["python", "sensor_simulator_v2.py"]
