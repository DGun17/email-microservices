import pika
import json
from lololo import send as send_email

connect = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

channel = connect.channel()

channel.exchange_declare(
    exchange='logs',
    exchange_type='fanout'
)

queue = channel.queue_declare(exclusive=True)

queue_name = queue.method.queue

print(f"[*] Starting worker email sender with name {queue_name}")

channel.queue_bind(exchange='logs', queue=queue_name)


def callback(ch, method, properties, body):
    log_data = json.loads(body)

    if log_data['type'] == 'error':
        print("[!] Error log detected, sending email ...")
        email_body = f"""
        Un error se ha detectado en el portal en el tiempo {log_data['date_time']}, el mensaje es: \n
        {log_data['message']}
        """

        reciver_email = [{'name': 'jaime', 'email': "jrnp1997@gmail.com"}, ]

        send_email(subject="Error detected", send_list=reciver_email, body=email_body)


channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()
