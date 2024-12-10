#!/bin/bash

# Inicia o RabbitMQ em segundo plano
rabbitmq-server &

# Usuário e senha do RabbitMQ
USER="rabbitmq"
PASSWORD="rabbitmq"

# URL do RabbitMQ Management API
HOST="localhost"
PORT="15672"

# Aguarda o RabbitMQ inicializar
echo "Aguardando RabbitMQ inicializar..."
for i in {1..10}; do
    if curl -u rabbitmq:rabbitmq http://localhost:15672/api/overview &>/dev/null; then
        echo "RabbitMQ está pronto."
        break
    fi
    sleep 2
done

# Criando o exchange
echo "Criando exchange 'fm.fanout'..."
rabbitmqadmin -u $USER -p $PASSWORD declare exchange name=fm.fanout type=fanout durable=true

# Criando as queues
echo "Criando fila 'c'..."
rabbitmqadmin -u $USER -p $PASSWORD declare queue name=c durable=true

echo "Criando fila 'p'..."
rabbitmqadmin -u $USER -p $PASSWORD declare queue name=p durable=true

# Associando as queues ao exchange
echo "Associando fila 'c' ao exchange 'fm.fanout'..."
rabbitmqadmin -u $USER -p $PASSWORD declare binding source=fm.fanout destination=c destination_type=queue

echo "Associando fila 'p' ao exchange 'fm.fanout'..."
rabbitmqadmin -u $USER -p $PASSWORD declare binding source=fm.fanout destination=p destination_type=queue

# Listando os bindings
echo "Listando bindings..."
rabbitmqadmin -u $USER -p $PASSWORD list bindings

#Mantem o container em execução
tail -f /dev/null