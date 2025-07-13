from fastapi import FastAPI, Depends

from fastapi.security import OAuth2PasswordBearer
from core.auth import get_current_user
import router.auth as auth

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# BASE.metadata.drop_all(bind=engine)
# BASE.metadata.create_all(bind=engine)

# def get_db():
#     db = session()
#     try: yield db
#     finally: db.close()

@app.get("/")
def root():
    return {"Hello": "World"}

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@app.post("/chatroom")
def chat(token:str = Depends(oauth2_scheme)):
    user = get_current_user(token)
    return user
