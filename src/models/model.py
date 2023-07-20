from pydantic import BaseModel, ConstrainedFloat, root_validator


class MessageModel(BaseModel):
    user_id: int
    message: str

    class Config:
        orm_mode = True
