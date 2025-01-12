// src/components/ModelSelect.jsx

import React, { useState, useEffect } from 'react';

const models = [
  { name: 'o1-preview', label: 'o1-preview' },
  // Ajoutez d'autres modèles ici
  { name: 'gpt-3', label: 'GPT-3' },
  { name: 'gpt-neo', label: 'GPT-Neo' },
];

function ModelSelect({ selectedModel, setSelectedModel }) {
  useEffect(() => {
    const storedModel = localStorage.getItem('selectedModel');
    if (storedModel) {
      setSelectedModel(storedModel);
    }
  }, [setSelectedModel]);

  const handleChange = (e) => {
    setSelectedModel(e.target.value);
    localStorage.setItem('selectedModel', e.target.value);
  };

  return (
    <div>
      <label htmlFor="model-select" className="block mb-2 text-sm font-medium text-gray-300">
        Sélectionnez le modèle :
      </label>
      <select
        id="model-select"
        value={selectedModel}
        onChange={handleChange}
        className="w-full bg-gray-800 text-white p-2 rounded"
      >
        {models.map((model) => (
          <option key={model.name} value={model.name}>
            {model.label}
          </option>
        ))}
      </select>
    </div>
  );
}

export default ModelSelect;
