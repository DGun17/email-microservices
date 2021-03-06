import pika
import json

connect = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

channel = connect.channel()

channel.exchange_declare(
    exchange='logs',
    exchange_type='direct',
)

queue = channel.queue_declare(exclusive=True)

queue_name = queue.method.queue

channel.queue_bind(exchange='logs', queue=queue_name, routing_key="[Debug]")
channel.queue_bind(exchange='logs', queue=queue_name, routing_key="[Info]")
channel.queue_bind(exchange='logs', queue=queue_name, routing_key="[Warning]")
channel.queue_bind(exchange='logs', queue=queue_name, routing_key="[Error]")

print(f"[*] Starting worker logger with queue {queue_name}")


def callback(ch, method, properties, body):
    log_data = json.loads(body)
    print(f"[*] Save {log_data['type']} log")
    string = f"{log_data['type']}:{log_data['date_time']}:{log_data['message']}\n"
    with open('logs.log', 'a') as f:
        f.write(string)


channel.basic_consume(callback, queue=queue_name, no_ack=True)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    pass
finally:
    connect.close()

