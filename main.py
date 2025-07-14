from fastapi import FastAPI, Depends
import router.auth as auth
import router.chatroom as chatroom
import router.subscribe as subscribe
import router.webhook as webhook
from db import BASE,engine
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

# BASE.metadata.drop_all(bind=engine)
BASE.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"Hello": "World"}

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(chatroom.router,prefix="/chatroom",tags=["Chatroom"])
app.include_router(subscribe.router,prefix="/subscribe",tags=["Subscription"])
app.include_router(webhook.router,prefix="/webhook",tags=["Subscription"])

