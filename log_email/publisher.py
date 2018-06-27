import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # Connect and block other rabbit connects

channel = connection.channel()   # Make a communication channel

channel.exchange_declare(exchange='logs', exchange_type='fanout')


def get_info():
    t = input("Ingrese tipo de log: ")
    d = input("Ingrese fecha de creacion del log: ")
    m = input("Ingrese mensaje del log: ")

    return t, d, m


if __name__ == '__main__':
    tip, date, msg = get_info()
    message = dict({'type': tip, 'date_time': date, 'message': msg})

    channel.basic_publish(exchange='logs',
                          routing_key='',
                          body=json.dumps(message)
                          )

    connection.close()



