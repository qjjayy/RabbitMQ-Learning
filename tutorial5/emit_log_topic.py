#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# topic is similar to direct
# the routing algorithm behind a topic exchange is a message sent with a particular routing key
# will be delivered to all the queues that are bound with a matching binding key
channel.exchange_declare(exchange='topic_logs',
                         type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='topic_logs',
                      routing_key=routing_key,
                      body=message)

print ' [x] Sent %r:%r' % (routing_key, message)
connection.close()
