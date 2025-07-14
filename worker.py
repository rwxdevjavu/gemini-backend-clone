from redis import Redis
from rq import Queue, Worker
import os
# Returns all workers registered in this connection
REDIS_DOMAIN = os.getenv("REDIS_DOMAIN")

redis_conn = Redis(host=REDIS_DOMAIN, port=6379, db=0)
workers = Worker.all(connection=redis_conn)

# Returns all workers in this queue (new in version 0.10.0)
queue = Queue('default')
workers = Worker.all(queue=queue)
worker = workers[0]
print(worker.name)

print('Successful jobs: ' + worker.successful_job_count)
print('Failed jobs: ' + worker.failed_job_count)
print('Total working time: '+ worker.total_working_time)  