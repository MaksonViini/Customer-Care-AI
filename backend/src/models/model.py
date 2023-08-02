from pydantic import BaseModel


class MessageModel(BaseModel):
    user_id: int
    message: str

    class Config:
        orm_mode = True
