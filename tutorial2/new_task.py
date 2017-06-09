#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import pika

message = ' '.join(sys.argv[1:]) or "Hello World!"

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# make sure that the task_queue queue won't be lost even if RabbitMQ restarts
channel.queue_declare(queue='task_queue', durable=True)

channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2  # make message persistent
                      ))
print " [x] Sent %r" % message

connection.close()
