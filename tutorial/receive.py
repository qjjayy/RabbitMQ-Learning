#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pika

# the same as send
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print " [x] Received %r" % body

# tell RabbitMQ that this particular callback function
# should receive messages from our hello queue
channel.basic_consume(callback, queue='hello', no_ack=True)

print " [*] Waiting for messages. To exit press CTRL+C"
channel.start_consuming()

