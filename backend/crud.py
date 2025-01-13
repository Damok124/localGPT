# backend/crud.py

from sqlalchemy.orm import Session
from . import models, schemas

def get_conversation(db: Session, conversation_id: int):
    return db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()

def get_conversations(db: Session):
    return db.query(models.Conversation).all()

def create_conversation(db: Session):
    db_conversation = models.Conversation()
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def create_message(db: Session, message: schemas.MessageCreate, conversation_id: int):
    db_message = models.Message(**message.dict(), conversation_id=conversation_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(db: Session, conversation_id: int):
    return db.query(models.Message).filter(models.Message.conversation_id == conversation_id).all()
