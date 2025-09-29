import React, { useState, useRef, useEffect } from 'react';
import { PaperAirplaneIcon, TrashIcon } from '@heroicons/react/24/outline';
import { useChat } from '../hooks/useChat';
import LoadingSpinner from './LoadingSpinner';
import MarkdownRenderer from './MarkdownRenderer';

const ChatInterface: React.FC = () => {
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { messages, isLoading, sendMessage, clearMessages } = useChat();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const message = inputMessage.trim();
    setInputMessage('');
    await sendMessage(message);
  };

  const formatTimestamp = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-md border border-gray-200">
      {/* Chat Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">MCP Gateway Chat</h3>
          <p className="text-sm text-gray-500">
            Ask questions about your registered services
          </p>
        </div>
        {messages.length > 0 && (
          <button
            onClick={clearMessages}
            className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-md transition-colors"
            title="Clear chat history"
          >
            <TrashIcon className="h-5 w-5" />
          </button>
        )}
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500">
            <div className="text-center">
              <div className="text-4xl mb-4">💬</div>
              <p className="text-lg font-medium">Start a conversation</p>
              <p className="text-sm">
                Ask me about your registered services, their endpoints, or how to use them.
              </p>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.sender === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`max-w-xs lg:max-w-3xl px-4 py-3 rounded-lg shadow-sm ${
                  message.sender === 'user'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-50 text-gray-900 border border-gray-200'
                }`}
              >
                {/* Message Avatar and Sender */}
                <div className="flex items-center mb-2">
                  <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium mr-2 ${
                    message.sender === 'user' 
                      ? 'bg-primary-500 text-white' 
                      : 'bg-primary-100 text-primary-700'
                  }`}>
                    {message.sender === 'user' ? '👤' : '🤖'}
                  </div>
                  <span className={`text-xs font-medium ${
                    message.sender === 'user' ? 'text-primary-100' : 'text-gray-600'
                  }`}>
                    {message.sender === 'user' ? 'You' : 'MCP Assistant'}
                  </span>
                </div>

                {/* Message Content */}
                <div className="text-sm">
                  {message.sender === 'user' ? (
                    <div className="whitespace-pre-wrap">{message.content}</div>
                  ) : (
                    <MarkdownRenderer 
                      content={message.content} 
                      className={message.sender === 'assistant' ? 'text-gray-900' : ''}
                    />
                  )}
                </div>

                {/* Tools Used Badge */}
                {message.tools_used && message.tools_used.length > 0 && (
                  <div className="mt-3 pt-2 border-t border-gray-300">
                    <div className="flex items-center text-xs text-gray-600 mb-2">
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 mr-2">
                        🔧 {message.tools_used.length} tool{message.tools_used.length > 1 ? 's' : ''} used
                      </span>
                    </div>
                    <details className="cursor-pointer">
                      <summary className="text-xs text-gray-500 hover:text-gray-700 font-medium">
                        View tools used
                      </summary>
                      <div className="mt-2 pl-2">
                        <ul className="space-y-1">
                          {message.tools_used.map((tool, index) => (
                            <li key={index} className="text-xs text-gray-600 flex items-center">
                              <span className="w-1.5 h-1.5 bg-blue-400 rounded-full mr-2"></span>
                              <code className="bg-gray-100 px-1 py-0.5 rounded text-xs font-mono">
                                {tool}
                              </code>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </details>
                  </div>
                )}

                {/* Timestamp */}
                <div className="flex items-center justify-between mt-2">
                  <div
                    className={`text-xs ${
                      message.sender === 'user'
                        ? 'text-primary-200'
                        : 'text-gray-400'
                    }`}
                  >
                    {formatTimestamp(message.timestamp)}
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="max-w-xs lg:max-w-3xl px-4 py-3 rounded-lg shadow-sm bg-gray-50 text-gray-900 border border-gray-200">
              <div className="flex items-center mb-2">
                <div className="w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium mr-2 bg-primary-100 text-primary-700">
                  🤖
                </div>
                <span className="text-xs font-medium text-gray-600">
                  MCP Assistant
                </span>
              </div>
              <div className="flex items-center space-x-2">
                <LoadingSpinner size="sm" />
                <span className="text-sm text-gray-500 italic">Thinking...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Message Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={!inputMessage.trim() || isLoading}
            className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <PaperAirplaneIcon className="h-5 w-5" />
          </button>
        </div>
        
        <div className="mt-3 flex flex-wrap gap-2">
          <div className="text-xs text-gray-500 mb-2 w-full">
            💡 Quick suggestions:
          </div>
          {[
            "List all employees",
            "What services are available?", 
            "Show me the API endpoints",
            "How do I create a new employee?",
            "What can you help me with?"
          ].map((suggestion, index) => (
            <button
              key={index}
              onClick={() => setInputMessage(suggestion)}
              disabled={isLoading}
              className="px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;
