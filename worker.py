import pika
import json
from lololo import mail as cus_mail
from email_django import message as django_mail

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue="emails")


def email(channel, method, properties, body):
    mail = json.loads(body)
    print(f" Send message ... to {mail['Para']} #{method.delivery_tag}")

    django_mail('Worker rabbitmq', mail['Para'], mail['De'], mail['Body'])
    # cus_mail('Worker rabbitmq', mail['Para'], mail['De'], mail['Body'])


channel.basic_consume(email, queue='emails', no_ack=True)


print("Worker start...")

channel.start_consuming()
