import datetime
from celery import Celery
import os
import models_db
import al_db
from sqlalchemy.orm import Session

rabbit_host = os.environ.get("RABBIT_HOST", "localhost")
app = Celery('celery_working', broker=f'pyamqp://guest@{rabbit_host}//')

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
    rekord1 = models_db.Currency(bank="GGG", currency="USD", date_exchange="2020-01-01", buy_rate=1.1, sale_rate=1.2)
    with Session(al_db.engine) as session:
        session.add(rekord1)
        session.commit()
    return x + y