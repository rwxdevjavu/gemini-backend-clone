from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
import bcrypt

from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def create_access_token(data):
    exp = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode = data.copy()
    to_encode['exp'] = exp
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token):
    try:
        return jwt.decode(token, SECRET_KEY , algorithms=[ALGORITHM])
    except JWTError as e:
        return e


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")  # store as string in DB

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

# token = create_access_token({"sub":"123"})
# payload = get_current_user("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMifQ.NQmrOijuwbvs5M2JvllEAMU089KzM6y5agLVPEaQ21I")
# print(token,payload)

