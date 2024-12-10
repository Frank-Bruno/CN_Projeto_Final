#!/usr/bin/env python
import pika
import pika.credentials

cred = pika.credentials.PlainCredentials("rabbitmq","rabbitmq")
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost",credentials=cred))
channel = connection.channel()

#channel.queue_declare(queue='teste1')

channel.basic_publish(exchange='fm.fanout', routing_key='', body='Hello World 1!')
channel.basic_publish(exchange='fm.fanout', routing_key='', body='Hello World 2!')
channel.basic_publish(exchange='fm.fanout', routing_key='', body='Hello World 3!')
print(" [x] Sent 'Hello World!'")
connection.close()