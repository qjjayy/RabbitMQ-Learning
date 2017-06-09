#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pika
import uuid


class FibonacciRpcClient(object):
    def __init__(self):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        # create an anonymous queue for callback
        # and dispose the response from the created queue
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response,
                                   queue=self.callback_queue,
                                   no_ack=True
                                   )

    def on_response(self, ch, method, props, body):
        # if we see an unknown correlation_id value, we may safely discard the message
        if self.corr_id == props.correlation_id:
            self.response = body

    # send a message to the rpc_queue with the properties which specify the response queue
    # and the correlation_id
    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id
                                   ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

print " [x] Requesting fib(30)"
response = fibonacci_rpc.call(30)
print " [.] Got %r" % response
