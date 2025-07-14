from fastapi import HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from redis import Redis

redis = Redis(port=6379,decode_responses=True)

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
