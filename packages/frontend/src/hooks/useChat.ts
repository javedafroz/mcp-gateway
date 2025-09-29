import { useState, useCallback } from 'react';
import { apiService } from '../services/api';
import type { ChatContextType } from '../types';

export const useChat = (): ChatContextType => {
  const [messages, setMessages] = useState<ChatContextType['messages']>([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = useCallback(async (message: string) => {
    if (!message.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      content: message,
      sender: 'user' as const,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await apiService.sendChatMessage({
        message,
        session_id: `session_${Date.now()}`,
      });

      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        content: response.response,
        sender: 'assistant' as const,
        timestamp: new Date(),
        tools_used: response.tools_used,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        content: `Error: ${error instanceof Error ? error.message : 'Failed to send message'}`,
        sender: 'assistant' as const,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  return {
    messages,
    isLoading,
    sendMessage,
    clearMessages,
  };
};

export default useChat;
