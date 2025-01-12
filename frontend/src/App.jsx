// src/App.jsx

import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';

function App() {
  const [conversationId, setConversationId] = useState(null);
  const [selectedModel, setSelectedModel] = useState('o1-preview');

  return (
    <div className="flex h-screen">
      <Sidebar
        conversationId={conversationId}
        setConversationId={setConversationId}
        selectedModel={selectedModel}
        setSelectedModel={setSelectedModel}
      />
      <ChatWindow
        conversationId={conversationId}
        selectedModel={selectedModel}
      />
    </div>
  );
}

export default App;
