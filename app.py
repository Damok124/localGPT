# app.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    content: str

@app.post("/chat/")
async def chat(message: Message):
    # Pour simplifier, nous renvoyons le message inversé
    response = message.content[::-1]
    return {"response": response}
