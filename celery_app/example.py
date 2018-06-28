from celery import Celery

app = Celery("example", backend='amqp://guest:guest@localhost', broker='amqp://localhost')


@app.task
def add(x, y):
    return x + y
