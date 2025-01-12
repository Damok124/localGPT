// src/components/ConversationsList.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ConversationsList({ conversationId, setConversationId }) {
  const [conversations, setConversations] = useState([]);

  useEffect(() => {
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    try {
      const response = await axios.get('http://localhost:8000/conversations/');
      setConversations(response.data);
    } catch (error) {
      console.error('Error fetching conversations', error);
    }
  };

  const createNewConversation = async () => {
    try {
      const response = await axios.post('http://localhost:8000/conversations/');
      const newConversation = response.data;
      setConversations([newConversation, ...conversations]);
      setConversationId(newConversation.id);
    } catch (error) {
      console.error('Error creating new conversation', error);
    }
  };

  const handleSelectConversation = (conversation) => {
    setConversationId(conversation.id);
  };

  return (
    <div>
      <button
        className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4"
        onClick={createNewConversation}
      >
        + Nouvelle conversation
      </button>
      <ul className="mt-2">
        {conversations.map((conversation) => (
          <li
            key={conversation.id}
            onClick={() => handleSelectConversation(conversation)}
            className={`p-4 cursor-pointer ${
              conversationId === conversation.id ? 'bg-gray-700' : 'hover:bg-gray-800'
            }`}
          >
            Conversation {conversation.id}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ConversationsList;
