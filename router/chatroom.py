from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
# from db import get_db
from core.auth import get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/")
def chat(token:str = Depends(oauth2_scheme)):
    user = get_current_user(token)
    return user