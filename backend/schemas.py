# backend/schemas.py

from pydantic import BaseModel
from typing import List

class MessageBase(BaseModel):
    sender: str
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    conversation_id: int

    class Config:
        orm_mode = True

class ConversationBase(BaseModel):
    pass

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int
    messages: List[Message] = []

    class Config:
        orm_mode = True
