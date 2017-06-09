#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pika
import time


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)


def callback(ch, method, properties, body):
    print " [x] Received %r" % body
    time.sleep(body.count(b'.'))
    print " [x] Done"
    # if the workers occasionally die without sending an ack,
    # there are other consumers online at the same time,
    # it will quickly redeliver it to another consumer,
    # so, it can make sure that no message is lost.
    ch.basic_ack(delivery_tag=method.delivery_tag)

# it don't dispatch a new message to a worker until it has processed
# and acknowledged the previous one
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='task_queue')

print " [*] Waiting for messages. To exit press CTRL+C"
channel.start_consuming()
