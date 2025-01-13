// src/components/SettingsModal.jsx

import React, { useState, useEffect } from 'react';

const models = [
  { name: 'o1-preview', label: 'o1-preview' },
  // Ajoutez d'autres modèles si nécessaire
];

function SettingsModal({ isOpen, onClose, selectedModel, setSelectedModel }) {
  const [apiKey, setApiKey] = useState('');

  useEffect(() => {
    const storedApiKey = localStorage.getItem('apiKey') || '';
    setApiKey(storedApiKey);
  }, []);

  const handleSave = () => {
    localStorage.setItem('apiKey', apiKey);
    localStorage.setItem('selectedModel', selectedModel);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white text-black rounded p-6 w-96">
        <h2 className="text-xl font-bold mb-4">Paramètres</h2>
        <div className="mb-4">
          <label htmlFor="model-select" className="block mb-2 text-sm font-medium">
            Modèle par défaut :
          </label>
          <select
            id="model-select"
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="w-full bg-gray-200 p-2 rounded"
          >
            {models.map((model) => (
              <option key={model.name} value={model.name}>
                {model.label}
              </option>
            ))}
          </select>
        </div>
        <div className="mb-4">
          <label htmlFor="api-key" className="block mb-2 text-sm font-medium">
            Clé API :
          </label>
          <input
            type="password"
            id="api-key"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            className="w-full bg-gray-200 p-2 rounded"
          />
        </div>
        <div className="flex justify-end">
          <button
            className="mr-2 px-4 py-2 bg-gray-300 rounded"
            onClick={onClose}
          >
            Annuler
          </button>
          <button
            className="px-4 py-2 bg-blue-500 text-white rounded"
            onClick={handleSave}
          >
            Enregistrer
          </button>
        </div>
      </div>
    </div>
  );
}

export default SettingsModal;
