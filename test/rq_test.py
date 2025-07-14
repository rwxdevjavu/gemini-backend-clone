from redis import Redis
from rq import Queue
from rq.job import Job

# Connect to Redis
redis_conn = Redis(host='localhost', port=6379, db=0)

# Specify the queue name
queue_name = 'default'  # Replace with your queue name if different
queue = Queue(name=queue_name, connection=redis_conn)

# List all jobs in the queue
jobs = queue.jobs

print(f"Jobs in the '{queue_name}' queue:")
for job in jobs:
    print(f"Job ID: {job.id}, Status: {job.get_status()}, Description: {job.description}")
    # job.delete()
    
    

