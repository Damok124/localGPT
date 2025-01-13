# backend/app.py

from fastapi import FastAPI, Depends, HTTPException, Form, Request
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List

import models
import schemas
import crud
from .database import SessionLocal, engine

# Importer les modules pour le modèle de langage
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Créer les tables de la base de données
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Autoriser les requêtes CORS
origins = [
    "http://localhost",
    "http://localhost:5173",
    # Ajoutez d'autres origines si nécessaire
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dépendance pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fonction pour charger le modèle spécifié
from functools import lru_cache

@lru_cache(maxsize=None)
def load_model(model_name: str):
    tokenizer = AutoTokenizer.from_pretrained(f"path/to/{model_name}") ############ a changer ?
    model = AutoModelForCausalLM.from_pretrained(f"path/to/{model_name}")
    return tokenizer, model

# Endpoint pour créer une nouvelle conversation
@app.post("/conversations/", response_model=schemas.Conversation)
def create_conversation(db: Session = Depends(get_db)):
    return crud.create_conversation(db)

# Endpoint pour récupérer toutes les conversations
@app.get("/conversations/", response_model=List[schemas.Conversation])
def get_conversations(db: Session = Depends(get_db)):
    return crud.get_conversations(db)

# Endpoint pour récupérer les messages d'une conversation
@app.get("/conversations/{conversation_id}/messages/", response_model=List[schemas.Message])
def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    messages = crud.get_messages(db, conversation_id)
    if messages is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return messages

# Endpoint pour envoyer un message
@app.post("/conversations/{conversation_id}/messages/", response_model=schemas.Message)
def send_message(
    conversation_id: int,
    message: schemas.MessageCreate,
    model_name: str = Form("o1-preview"),
    request: Request = None,
    db: Session = Depends(get_db)
):
    # Récupérer la clé API depuis l'en-tête
    api_key = request.headers.get('x-api-key')

    # Vérifier si la conversation existe
    conversation = crud.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Sauvegarder le message de l'utilisateur
    user_message = crud.create_message(db, message, conversation_id)

    # Charger le modèle spécifié
    tokenizer, model = load_model(model_name)

    # Construire le contexte
    past_messages = crud.get_messages(db, conversation_id)
    context = ""
    for msg in past_messages:
        context += f"{msg.sender}: {msg.content}\n"

    # Générer la réponse du modèle
    inputs = tokenizer.encode(context + 'assistant:', return_tensors='pt')
    outputs = model.generate(inputs, max_length=1024, do_sample=True, temperature=0.7)
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True).split('assistant:')[-1].strip()

    # Sauvegarder le message de l'assistant
    assistant_message = schemas.MessageCreate(
        sender='assistant',
        content=response_text
    )
    assistant_message = crud.create_message(db, assistant_message, conversation_id)

    return assistant_message
