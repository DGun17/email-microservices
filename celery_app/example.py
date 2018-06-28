from celery import Celery

app = Celery("example", backend='amqp://guest:guest@localhost', broker='amqp://localhost')


@app.task(bind=True, exclusive=True)
def add(self, x, y):
    print(self)
    return x + y


class Multiply(app.Task):
    name = "Multiply"

    def run(self, x, y):
        return x * y


app.register_task(Multiply())

