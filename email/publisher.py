import json
import pika


def get_info():
    de = input("Ingrese email del redactor: ")
    para = input("Ingrese email destino: ")
    body = input("Ingrese mensaje: ")

    return de, para, body


if __name__ == "__main__":
    d, p, b = get_info()
    info = dict({
        'De': d,
        'Para': p,
        'Body': b
    })
    data = json.dumps(info)
    print(data)

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='emails')

    channel.basic_publish(
        exchange="",
        routing_key="emails",
        body=data
    )
