from pydantic import BaseModel


class MessageModel(BaseModel):
    user_id: str
    message: str

    class Config:
        orm_mode = True
