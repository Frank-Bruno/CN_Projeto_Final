# Instalação com Kubernets
Instala o pod do Rabbitmq
```sh
kubectl apply -f rabbitm-deployment  
```
Para acessar o Rabbitmq localmente faça um port-forward:
```sh
kubectl port-forward deployment/rabbitmq 15672:15672 
```

# Instalação com Docker
## Instalação Automática do RabbitMQ 

```sh
docker build -t my_rabbitmq_with_setup .

docker run -d --name rabbitmq -p 8080:15672 -p 5672:5672 -p 25676:25676 -e RABBITMQ_DEFAULT_USER=rabbitmq -e RABBITMQ_DEFAULT_PASS=rabbitmq my_rabbitmq_with_setup


```


## Instalação do RabbitMQ Manualmente


```sh
docker run -d --name my_rabbitmq -p 8080:15672 -p 5672:5672 -p 25676:25676 -e RABBITMQ_DEFAULT_USER=rabbitmq -e RABBITMQ_DEFAULT_PASS=rabbitmq rabbitmq:3.10.5-management
```
Dentro do conteiner execute 

```sh
#Criando exchange
rabbitmqadmin -u rabbitmq -p rabbitmq declare exchange name=fm.fanout type=fanout durable=true

#Criando queues
rabbitmqadmin -u rabbitmq -p rabbitmq declare queue name=c durable=true

rabbitmqadmin -u rabbitmq -p rabbitmq declare queue name=p durable=true

#Associando as queues ao exchange
rabbitmqadmin -u rabbitmq -p rabbitmq declare binding source=fm.fanout destination=c destination_type=queue

rabbitmqadmin -u rabbitmq -p rabbitmq declare binding source=fm.fanout destination=p destination_type=queue

#Mostra a lista de queues
rabbitmqadmin -u rabbitmq -p rabbitmq list bindings

```

Bibliotecas python

```
pip install pika
```