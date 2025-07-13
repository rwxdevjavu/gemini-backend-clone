from sqlalchemy import Column, Integer, String, Boolean
from db import BASE


class User(BASE):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    mobile_no = Column(String(10), unique=True, index=True)
    name = Column(String)
    password = Column(String)
    otp = Column(String)
    is_verified = Column(Boolean, default=False)
    is_paid = Column(Boolean, default=False)
    rate = Column(Integer,default=5)
    access_token = Column(String)


    def __init__(self,mobile_no,name,password,otp):
        self.mobile_no = mobile_no
        self.name = name
        self.password = password
        self.otp = otp

