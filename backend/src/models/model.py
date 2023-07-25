from pydantic import BaseModel, root_validator


class MessageModel(BaseModel):
    user_id: int
    message: str

    class Config:
        orm_mode = True
