// src/components/Sidebar.jsx

import React from 'react';
import ConversationsList from './ConversationList';
import ModelSelect from './ModelSelect';

function Sidebar({ conversationId, setConversationId, selectedModel, setSelectedModel }) {
  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col">
      <div className="p-4 border-b border-gray-700">
        <h1 className="text-2xl font-bold">localGPT</h1>
      </div>
      <div className="flex-1 overflow-y-auto">
        <ConversationsList
          conversationId={conversationId}
          setConversationId={setConversationId}
        />
      </div>
      <div className="p-4 border-t border-gray-700">
        <ModelSelect
          selectedModel={selectedModel}
          setSelectedModel={setSelectedModel}
        />
      </div>
    </div>
  );
}

export default Sidebar;
