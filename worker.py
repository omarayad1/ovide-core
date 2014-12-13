import pika
from modules import lint_verilog, compile_verilog, vvp_utils, wave_utils
import os

connection = pika.BlockingConnection(
    pika.URLParameters(os.environ["RABBIT_URL"])
)

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')


def on_request(ch, method, props, body):
    n = body

    print " [.] function: %s" % n

    response = eval(n)

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
        ),
        body=str(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print " [x] Awaiting RPC requests"
channel.start_consuming()