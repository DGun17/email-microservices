from celery import Celery
from lololo import send

app = Celery("sender_email", backend="amqp://guest:guest@localhost", broker="amqp://localhost")


@app.task
def sender(para, email_body):
    reciver_email = [{'name': 'jaime', 'email': para}, ]
    send(subject="Error detected", send_list=reciver_email, body=email_body)


def get_info():
    para = input("Ingrese email destino: ")
    body = input("Ingrese mensaje: ")

    return sender.delay(para, body)

