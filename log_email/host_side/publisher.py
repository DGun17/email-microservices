import pika
import json


def get_info():
    with open('../server_side/logs.log', 'r') as f:
        info = f.readlines()[-1].split('_')
        data = dict({'type': info[0], 'date_time': info[1], 'message': info[2]})

    return data


def run():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )  # Connect and block other rabbit connects

    channel = connection.channel()  # Make a communication channel

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    message = get_info()

    channel.basic_publish(exchange='logs',
                          routing_key='',
                          body=json.dumps(message)
                          )

    connection.close()
    return True



