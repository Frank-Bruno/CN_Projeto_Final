# Base image
FROM rabbitmq:3.10.5-management

# Copiar o script para dentro do container
COPY setup_rabbitmq.sh /scripts/setup_rabbitmq.sh

# Tornar o script executável
RUN chmod +x /scripts/setup_rabbitmq.sh

# Executar o script após iniciar o RabbitMQ
CMD ["sh", "-c", "/scripts/setup_rabbitmq.sh"]
