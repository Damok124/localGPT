from sqlalchemy.orm import Session
from models import Conversation, Message, Config
from schemas import MessageCreate


def get_conversation(db: Session, conversation_id: int):
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()

def get_conversations(db: Session):
    return db.query(Conversation).all()

def create_conversation(db: Session):
    db_conversation = Conversation()
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def create_message(db: Session, message: MessageCreate, conversation_id: int):
    db_message = Message(**message.dict(), conversation_id=conversation_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(db: Session, conversation_id: int):
    return db.query(Message).filter(Message.conversation_id == conversation_id).all()

def set_api_key(db: Session, api_key: str):
    config = db.query(Config).filter(Config.key == "api_key").first()
    if config:
        config.value = api_key
    else:
        config = Config(key="api_key", value=api_key)
        db.add(config)
    db.commit()

def get_api_key(db: Session):
    api_key = db.query(Config).filter(Config.key == 'api_key').first()
    print(f"Retrieved API key from DB: {api_key}")  # Vérifiez ce que retourne la base de données
    return api_key.value if api_key else None

