from sqlalchemy import Column, Integer, ForeignKey, Text,DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from db import BASE

class Message(BASE):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    chatroom_id = Column(Integer, ForeignKey("chatrooms.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_user = Column(Boolean, default=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    chatroom = relationship("Chatroom", back_populates="messages")

    def __init__(self,content,chatroom_id,is_user):
        self.content = content
        self.chatroom_id = chatroom_id
        self.is_user = is_user

