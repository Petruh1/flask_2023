import datetime
from celery import Celery

app = Celery('celery_working', broker='pyamqp://guest@localhost//')

# app.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': 'task.add',
#         'schedule': 5.0,
#         'args': (16, 16)
#     }
# }
# app.conf.timezone = 'UTC'

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, add.s(x=2, y=4), name='add every 10')

@app.task
def add(x, y):
    print(x + y)
    with open('test.txt', 'w') as f:
        f.write(f'x + y = {x + y} {datetime.datetime.now()}')
    return x + y