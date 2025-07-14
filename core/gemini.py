from celery import Celery
import redis
import json
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from db import engine
from google import genai
import os
from dotenv import load_dotenv
from models.message import Message

load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
celery_app = Celery("chatai", broker=REDIS_URL, backend=REDIS_URL)

redis_store = redis.Redis.from_url(REDIS_URL, decode_responses=True)

SessionLocal = sessionmaker(bind=engine)

@celery_app.task(name="tasks.request_gemini")
def request_gemini(contests:str,chatroom_id:int):
    db = SessionLocal()
    try:
        response = client.models.generate_content(model="gemini-2.5-flash",contents=contests)
        message = Message(response.text,chatroom_id,False)
        db.add(message)
        db.commit()
        return response.text
    except Exception as e:
        return "Something went wrong"
    finally:
        db.close()
