from schema.auth import SignupRequest ,SentOTP ,VeriftOTP ,SigninRequest
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException,status
from models.user import User
from db import get_db
from core.auth import hash_password,verify_password,create_access_token,get_current_user
from core.utils import generate_otp

router = APIRouter()


@router.post("/signup")
def signup(request:SignupRequest,db: Session = Depends(get_db)):
    user = db.query(User).filter_by(mobile_no=request.mobile_no).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already exists.")
    hashed = hash_password(request.password)
    user = User(request.mobile_no,request.name,hashed)
    db.add(user)
    db.commit();
    return {"success":True, "message":"User create successfully"}

@router.post("/send-otp")
def sendotp(request:SentOTP,db:Session = Depends(get_db)):
    user = db.query(User).filter_by(mobile_no=request.mobile_no).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    try:
        otp:str = generate_otp()
        user.otp = otp
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
    return {"success":True,"otp":user.otp}

@router.post("/verify-otp")
def verifyotp(request:VeriftOTP,db:Session = Depends(get_db)):
    user = db.query(User).filter_by(mobile_no=request.mobile_no).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user.otp == request.otp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid OTP")
    try:
        user.is_verified = True
        db.commit()    
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
    return {"success":True,"message":"OTP verified successfully"}
    
@router.post('/signin')
def signin(request:SigninRequest,db:Session = Depends(get_db)):
    user = db.query(User).filter_by(mobile_no=request.mobile_no).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    elif not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not verified")
    elif not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    try:
        access_token = create_access_token({"user_id":user.id,"mobile_no":user.mobile_no,"name":user.name})
        user.access_token = access_token
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
    return {"access_token": access_token, "token_type": "bearer"}
    
