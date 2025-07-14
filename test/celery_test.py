from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL")

app = Celery('celery_test', broker=REDIS_URL)

@app.task
def hello():
    return 'hello world'

hello.delay()

