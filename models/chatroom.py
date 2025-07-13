from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,func, Text, Boolean
from sqlalchemy.orm import relationship
from db import BASE

class Chatroom(BASE):
    __tablename__ = "chatrooms"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="chatrooms")
    messages = relationship("Message", back_populates="chatroom", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    def __init__(self,title,user_id):
        self.title = title
        self.user_id = user_id
