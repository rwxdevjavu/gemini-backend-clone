from fastapi import FastAPI, Depends, HTTPException,status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import session,BASE,engine
from fastapi.security import OAuth2PasswordBearer
from model import User
from utils import generate_otp
from auth import hash_password,verify_password,create_access_token,get_current_user

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# BASE.metadata.drop_all(bind=engine)
# BASE.metadata.create_all(bind=engine)

def get_db():
    db = session()
    try: yield db
    finally: db.close()

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


@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/auth/signup")
def signup(request:SignupRequest,db: Session = Depends(get_db)):
    user = db.query(User).filter_by(mobile_no=request.mobile_no).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already exists.")
    otp:str = generate_otp()
    hashed = hash_password(request.password)
    user = User(request.mobile_no,request.name,hashed,otp)
    db.add(user)
    db.commit();
    return {"success":True, "message":"User create successfully"}

@app.post("/auth/send-otp")
def sendotp(request:SentOTP,db:Session = Depends(get_db)):
    user = db.query(User).filter_by(mobile_no=request.mobile_no).first()
    if not user:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"success":True,"otp":user.otp}

@app.post("/auth/verify-otp")
def verifyotp(request:VeriftOTP,db:Session = Depends(get_db)):
    user = db.query(User).filter_by(mobile_no=request.mobile_no,otp = request.otp).first()
    if not user:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_verified = True
    db.commit()
    return {"success":True,"message":"OTP verified successfully"}
    
@app.post('/auth/signin')
def signin(request:SigninRequest,db:Session = Depends(get_db)):
    user = db.query(User).filter_by(mobile_no=request.mobile_no).first()
    try:
        if not user:
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        elif not user.is_verified:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not verified")
        elif not verify_password(request.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
        access_token = create_access_token({"user_id":user.id,"mobile_no":user.mobile_no,"name":user.name})
        user.access_token = access_token
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
    return {"access_token": access_token, "token_type": "bearer"}
    

@app.post("/chatroom")
def chat(token:str = Depends(oauth2_scheme)):
    user = get_current_user(token)
    return user
