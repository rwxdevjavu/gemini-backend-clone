from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from db import get_db
from core.auth import get_current_user
from models.user import User
from models.chatroom import Chatroom
from models.message import Message
from schema.chatroom import SendMessage
from fastapi.security import OAuth2PasswordBearer
from core.ratelimiter import rate_limit

import json
from redis import Redis 
from rq import Queue
from core.gemini import request_gemini
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_DOMAIN = os.getenv("REDIS_DOMAIN")

redis_conn = Redis(host=REDIS_DOMAIN, port=6379, db=0)
queue = Queue(connection=redis_conn)



router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("")
def get_chatrooms(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cache_key = f"chatrooms:{user.id}"
    cached_data = redis_conn.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    chats = db.query(Chatroom).filter_by(user_id = user.id).all()
    def serialize(chat):
        return {
            "id": chat.id,
            "title": chat.title,
            "created_at": str(chat.created_at),
        }

    chat_data = [serialize(chat) for chat in chats]

    redis_conn.setex(cache_key,300, json.dumps(chat_data))
    return chats

@router.post("")
def create_chatchat(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        chat = Chatroom("New Chat",user.id)
        db.add(chat)
        db.commit()
        return {"success": True, "message": "New Chat Created successfully"}
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

@router.get("/{id}")
def get_chatroom_messages(id: int,user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chatroom = db.query(Chatroom).filter_by(user_id = user.id,id = id).first()
    if not chatroom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    messages = db.query(Message).filter_by(chatroom_id = chatroom.id).all()
    return messages

@router.post("/{id}/message")
def get_chatroom_messages(id: int,request:SendMessage,user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rate_limit(user)
    chatroom = db.query(Chatroom).filter_by(user_id = user.id,id = id).first()
    if not chatroom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    try:
        message = Message(request.message,chatroom.id,True)
        db.add(message)
        db.commit();
        job = request_gemini.apply_async(args=[request.message, chatroom.id])
        return { "Success":True, "message":"generating response","job_id":job.id }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="AI couldnot generate prompt please try again")
