import pika
import subprocess

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')


def get_file_link(n):
    return n


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def check_for_errors(n):
    p = subprocess.Popen(
        ["bin/verilator --lint-only %s" % n],
        stdout=subprocess.PIPE,
        shell=True,
        stderr=subprocess.STDOUT
    )
    data, err = p.communicate()
    return data, err


def on_request(ch, method, props, body):
    n = body

    print " [.] filename: %s" % n

    response, err = check_for_errors(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id
                     ),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print " [x] Awaiting RPC requests"
channel.start_consuming()