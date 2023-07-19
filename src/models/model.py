from pydantic import BaseModel, ConstrainedFloat, root_validator


class MessageModel(BaseModel):
    message: str

    class Config:
        orm_mode = True
