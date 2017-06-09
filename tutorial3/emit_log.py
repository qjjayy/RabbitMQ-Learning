#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create an exchange that will broadcast all the messages
# it receives to all the queues it knows
channel.exchange_declare(exchange='logs', type='fanout')

# publish messages to our named exchange instead
message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)

print " [x] Sent %r" % message
connection.close()
