from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship, declarative_base
from db import BASE


class User(BASE):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    mobile_no = Column(String(10), unique=True, index=True)
    name = Column(String)
    password = Column(String)
    otp = Column(String)
    is_verified = Column(Boolean, default=False)
    is_pro = Column(Boolean, default=False)
    rate = Column(Integer,default=5)
    access_token = Column(String)
    chatrooms = relationship("Chatroom", back_populates="owner", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=func.now())


    def __init__(self,mobile_no,name,password):
        self.mobile_no = mobile_no
        self.name = name
        self.password = password

