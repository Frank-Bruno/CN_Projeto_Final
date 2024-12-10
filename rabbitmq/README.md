# Instalação do RabbitMQ


```
docker run -d --name my_rabbitmq -p 8080:15672 -p 5672:5672 -p 25676:25676 -e RABBITMQ_DEFAULT_USER=rabbitmq -e RABBITMQ_DEFAULT_PASS=rabbitmq rabbitmq:3.10.5-management
```
Bibliotecas python

```
pip install pika
```