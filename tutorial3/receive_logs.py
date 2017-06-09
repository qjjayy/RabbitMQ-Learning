#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', type='fanout')

# first, create a queue with a random name, which is decided by the server
# second, once we disconnect the consumer the queue should be deleted(exclusive=True)
result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue

# bind the exchange to the queue
channel.queue_bind(exchange='logs', queue=queue_name)

print " [*] Waiting for logs. To exit press CTRL+C"


def callback(ch, method, properties, body):
    print " [x] %r" % body

channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()
