from pydantic import BaseModel

class SendMessage(BaseModel):
    message: str

