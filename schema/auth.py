from pydantic import BaseModel

class SignupRequest(BaseModel):
    mobile_no: str
    password: str
    name:str

class SigninRequest(BaseModel):
    mobile_no:str
    password:str

class SentOTP(BaseModel):
    mobile_no: str

class VeriftOTP(BaseModel):
    mobile_no: str
    otp:str

