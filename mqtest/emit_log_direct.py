#!/usr/bin/python
import pika
import sys


credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters('11.11.11.11',5672,'testhost',credentials))


channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'

message = ' '.join(sys.argv[2:]) or "info: Hello World!"

channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)

print(" [x] Sent %r:%r" % (severity, message))
connection.close()


