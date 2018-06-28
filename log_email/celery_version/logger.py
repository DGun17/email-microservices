import json
from celery import Celery
from kombu import Queue, Exchange
from lololo import send as send_email

ex_logs = Exchange('poper3', 'fanout')

app = Celery("logger", backend="amqp://guest:guest@localhost", broker="amqp://localhost")

# logs = Queue(exclusive=True, exchange=ex_logs)
# error_notify = Queue(exclusive=True, exchange=ex_logs)


app.conf.task_queues = (
    Queue('loogs', exchange=ex_logs),
    Queue('errors', exchange=ex_logs),
)

app.conf.task_default_exchange = ex_logs


@app.task(queue='loogs', exchange=ex_logs)
def logs(body):
    log_data = json.loads(body)
    string = f"{log_data['type']}:{log_data['date_time']}:{log_data['message']}\n"
    with open('logs.log', 'a') as f:
        f.write(string)


@app.task(queue='errors')
def error_notify(body):
    log_data = json.loads(body)
    if log_data['type'] == '[Error]':
        email_body = f"""
                Un error se ha detectado en el portal en el tiempo {log_data['date_time']}, el mensaje es: \n
                {log_data['message']}
                """
        reciver_email = [{'name': 'jaime', 'email': "jrnp1997@gmail.com"}, ]
        send_email(subject="Error detected", send_list=reciver_email, body=email_body)


class Logger(app.Task):
    name = "Logger"

    def run(self):
        with open('server_side/logs.log', 'r') as f:
            info = f.readlines()[-1].split('_')
            data = dict({'type': info[0], 'date_time': info[1], 'message': info[2]})
        return data


app.register_task(Logger())
