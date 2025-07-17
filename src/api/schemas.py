from pydantic import BaseModel
from typing import Optional
from datetime import date


class Message(BaseModel):
    message_id: int
    date: date
    text: Optional[str]
    file_path: Optional[str]
    channel: str

    class Config:
        orm_mode = True


class Detection(BaseModel):
    message_id: int
    channel: str
    class_name: str
    confidence: float

    class Config:
        orm_mode = True


class ChannelActivity(BaseModel):
    channel: str
    total_messages: int
    first_post_date: date
    last_post_date: date

    class Config:
        orm_mode = True
        
