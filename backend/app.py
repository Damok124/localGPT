from flask import Flask, jsonify
from flask_cors import CORS
import logging
from sqlalchemy.orm import Session
import crud
from database import SessionLocal
import models

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Autoriser toutes les origines (ou configurer spécifiquement)

# Configurer les logs
logging.basicConfig(level=logging.DEBUG)

# Initialisation de la clé API
def init_api_key():
    db = SessionLocal()
    api_key = crud.get_api_key(db)
    if not api_key:
        logging.error("API key not configured.")
        return ""
    return api_key

# Fonction pour récupérer les conversations
@app.route('/conversations/', methods=['GET'])
def get_conversations():
    try:
        db = SessionLocal()
        conversations = crud.get_conversations(db)
        if not conversations:
            logging.info("No conversations found.")
            return jsonify([])  # Retourne une liste vide si aucune conversation
        return jsonify([conversation.to_dict() for conversation in conversations])
    except Exception as e:
        logging.error(f"Error fetching conversations: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Fonction pour envoyer un message et obtenir une réponse d'OpenAI
@app.route('/send_message/', methods=['POST'])
def send_message():
    data = request.get_json()
    conversation_id = data.get("conversation_id")
    message_content = data.get("message_content")
    
    if not conversation_id or not message_content:
        logging.warning("Missing required parameters (conversation_id or message_content).")
        return jsonify({"error": "Missing parameters"}), 400

    try:
        db = SessionLocal()
        # Vérifier si la conversation existe
        conversation = crud.get_conversation(db, conversation_id)
        if not conversation:
            logging.warning(f"Conversation with ID {conversation_id} not found.")
            return jsonify({"error": "Conversation not found."}), 404
        
        # Sauvegarder le message utilisateur
        user_message = crud.create_message(db, models.MessageCreate(sender="user", content=message_content), conversation_id)

        # Construire le contexte pour OpenAI
        past_messages = crud.get_messages(db, conversation_id)
        messages_for_api = [{"role": "user" if m.sender == "user" else "assistant", "content": m.content} for m in past_messages]
        messages_for_api.append({"role": "user", "content": message_content})

        # Appeler l'API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_for_api,
            temperature=0.7
        )
        assistant_response = response['choices'][0]['message']['content']
        logging.info(f"Assistant: {assistant_response}")

        # Sauvegarder la réponse de l'assistant
        assistant_message = models.MessageCreate(sender="assistant", content=assistant_response)
        crud.create_message(db, assistant_message, conversation_id)

        return jsonify({"response": assistant_response})
    except Exception as e:
        logging.error(f"Error sending message: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Initialiser le serveur Flask
@app.route('/')
def home():
    return "Welcome to LocalGPT Backend!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Démarrer le serveur Flask sur le port 5000
