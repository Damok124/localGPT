// src/components/Message.jsx
import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { materialLight } from 'react-syntax-highlighter/dist/esm/styles/prism';

function Message({ message }) {
  const isUser = message.sender === 'user';

  const parseContent = (content) => {
    const codeBlockRegex = /```([a-zA-Z]*)\n([\s\S]*?)```/g;
    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = codeBlockRegex.exec(content)) !== null) {
      const [fullMatch, language, code] = match;
      const index = match.index;

      // Texte avant le bloc de code
      if (index > lastIndex) {
        parts.push({
          type: 'text',
          content: content.substring(lastIndex, index),
        });
      }

      // Bloc de code
      parts.push({
        type: 'code',
        language: language || 'plaintext',
        content: code,
      });

      lastIndex = index + fullMatch.length;
    }

    // Texte après le dernier bloc de code
    if (lastIndex < content.length) {
      parts.push({
        type: 'text',
        content: content.substring(lastIndex),
      });
    }

    return parts;
  };

  const messageContent = parseContent(message.content);

  return (
    <div className={`p-4 ${isUser ? 'bg-white text-right' : 'bg-gray-100 text-left'}`}>
      <div className="max-w-2xl mx-auto">
        {messageContent.map((part, index) => {
          if (part.type === 'text') {
            return <p key={index} className="mb-2">{part.content}</p>;
          } else if (part.type === 'code') {
            return (
              <div key={index} className="my-2">
                <SyntaxHighlighter language={part.language} style={materialLight}>
                  {part.content}
                </SyntaxHighlighter>
              </div>
            );
          }
          return null;
        })}
      </div>
    </div>
  );
}

export default Message;
