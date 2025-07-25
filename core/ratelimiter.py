from fastapi import HTTPException,status
from redis import Redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_DOMAIN = os.getenv("REDIS_DOMAIN")
redis = Redis(host=REDIS_DOMAIN,port=6379,decode_responses=True)

def rate_limit(user):
    if user.is_pro:
        return
    key = f"limit:{user.id}"
    max_request = 5
    time = 86400

    current = redis.get(key)
    if current is None:
        redis.set(key,1,ex=time)
    elif int(current) < max_request:
        redis.incr(key)
    else:
        ttl = redis.ttl(key)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,detail="5 request/day for free"
        )
