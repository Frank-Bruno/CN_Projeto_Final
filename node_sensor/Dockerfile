FROM python:3.9-slim

WORKDIR /app

COPY sensor_simulator.py .

RUN pip install pika influxdb-client

CMD ["python", "sensor_simulator.py"]