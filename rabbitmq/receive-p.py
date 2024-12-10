#!/usr/bin/env python
import pika, sys, os

import pika.credentials

def main():
    cred = pika.credentials.PlainCredentials("rabbitmq","rabbitmq")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost",credentials=cred))
    channel = connection.channel()

    #channel.queue_declare(queue='teste1')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue='p', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)