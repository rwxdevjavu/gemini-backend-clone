from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
from models.message import Message

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def request_gemini(contests:str,chatroom_id:int):
    from sqlalchemy.orm import sessionmaker
    from db import engine
    SessionLocal = sessionmaker(bind=engine)
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

