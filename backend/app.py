from flask import Flask
import logging
from sqlalchemy.orm import Session
import crud
from database import SessionLocal
import models

# Initialisation de la clé API
def init_api_key():
    db = SessionLocal()
    api_key = crud.get_api_key(db)
    if not api_key:
        print("API key not configured.")
        return ""
    return api_key

# Fonction pour récupérer les conversations
def get_conversations():
    db = SessionLocal()
    conversations = crud.get_conversations(db)
    for conversation in conversations:
        print(f"Conversation ID: {conversation.id}")
        for message in conversation.messages:
            print(f"  {message.sender}: {message.content}")

# Fonction pour envoyer un message et obtenir une réponse d'OpenAI
def send_message(conversation_id, message_content):
    db = SessionLocal()
    
    # Vérifier si la conversation existe
    conversation = crud.get_conversation(db, conversation_id)
    if not conversation:
        print("Conversation not found.")
        return
    
    # Sauvegarder le message utilisateur
    user_message = crud.create_message(db, models.MessageCreate(sender="user", content=message_content), conversation_id)

    # Construire le contexte pour OpenAI
    past_messages = crud.get_messages(db, conversation_id)
    messages_for_api = [{"role": "user" if m.sender == "user" else "assistant", "content": m.content} for m in past_messages]
    messages_for_api.append({"role": "user", "content": message_content})

    # Appeler l'API OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_for_api,
            temperature=0.7
        )
        assistant_response = response['choices'][0]['message']['content']
        print(f"Assistant: {assistant_response}")
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")

    # Sauvegarder la réponse de l'assistant
    assistant_message = models.MessageCreate(sender="assistant", content=assistant_response)
    crud.create_message(db, assistant_message, conversation_id)

# Initialiser le serveur Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to LocalGPT Backend!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Démarrer le serveur Flask sur le port 5000
