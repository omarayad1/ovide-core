import pika
import os

connection = pika.BlockingConnection(
    pika.URLParameters(os.environ["RABBIT_URL"])
)

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

channel.queue_delete(queue='rpc_queue')
channel.close()
connection.close()