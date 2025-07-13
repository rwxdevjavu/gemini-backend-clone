from fastapi import FastAPI, Depends
import router.auth as auth
import router.chatroom as chatroom

app = FastAPI()

# BASE.metadata.drop_all(bind=engine)
# BASE.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"Hello": "World"}

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(chatroom.router,prefix="/chatroom",tags=["Chatroom"])

