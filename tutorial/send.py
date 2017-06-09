#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pika

# establish a connection with RAbbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create a hello queue to which the message will be delivered
channel.queue_declare(queue='hello')

# exchange: specify exactly to which queue the message should go
# default exchange is identified by an empty string
# routing_key: specify the queue name
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print "[x] Sent 'Hello World!'"

# close the connection
connection.close()

