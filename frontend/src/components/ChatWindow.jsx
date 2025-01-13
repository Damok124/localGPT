// src/components/ChatWindow.jsx

import React, { useState, useEffect, useRef } from 'react';
import Message from './Message';
import axios from 'axios';

function ChatWindow({ conversationId, selectedModel }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const apiKey = localStorage.getItem('apiKey') || '';

  useEffect(() => {
    if (conversationId) {
      fetchMessages(conversationId);
    } else {
      setMessages([]);
    }
  }, [conversationId]);

  const fetchMessages = async (id) => {
    try {
      const response = await axios.get(`http://localhost:8000/conversations/${id}/messages/`);
      setMessages(response.data);
      scrollToBottom();
    } catch (error) {
      console.error('Error fetching messages', error);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || !conversationId) return;

    const userMessage = {
      conversation_id: conversationId,
      sender: 'user',
      content: input,
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');
    scrollToBottom();

    try {
		const response = await axios.post(
		  `http://localhost:8000/conversations/${conversationId}/messages/`,
		  {
			conversation_id: conversationId,
			sender: 'user',
			content: input,
		  },
		  {
			headers: {
			  'x-api-key': apiKey,
			  'Content-Type': 'application/json',
			},
			params: {
			  model_name: selectedModel,
			},
		  }
		);

      const assistantMessage = response.data;
      setMessages((prevMessages) => [...prevMessages, assistantMessage]);
      scrollToBottom();
    } catch (error) {
      console.error('Error sending message', error);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="flex-1 flex flex-col bg-gray-50">
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((message, index) => (
          <Message key={index} message={message} />
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="p-4 border-t border-gray-300">
        <textarea
          className="w-full p-2 border rounded resize-none"
          rows="2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Tapez votre message..."
        ></textarea>
        <button
          className="mt-2 w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded"
          onClick={sendMessage}
        >
          Envoyer
        </button>
      </div>
    </div>
  );
}

export default ChatWindow;
