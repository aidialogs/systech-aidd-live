'use client';

import { useState, useEffect, FormEvent } from 'react';
import { Send, Bot, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  ChatBubble,
  ChatBubbleAvatar,
  ChatBubbleMessage,
} from '@/components/ui/chat-bubble';
import { ChatInput } from '@/components/ui/chat-input';
import { ChatMessageList } from '@/components/ui/chat-message-list';
import { sendChatMessage, getChatHistory } from '@/lib/api';

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  sql_query?: string;
}

interface ChatInterfaceProps {
  userId: number;
  chatId: number;
  mode: 'normal' | 'admin';
  loadHistoryOnMount?: boolean; // Optional: whether to load history on mount
}

export function ChatInterface({ 
  userId, 
  chatId, 
  mode, 
  loadHistoryOnMount = true 
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load history on mount (only if enabled)
  useEffect(() => {
    if (loadHistoryOnMount) {
      loadHistory();
    }
  }, [userId, chatId, loadHistoryOnMount]);

  const loadHistory = async () => {
    try {
      const history = await getChatHistory(userId, chatId);
      const formattedMessages = history.map((msg, idx) => ({
        id: idx,
        role: msg.role as 'user' | 'assistant',
        content: msg.content,
      }));
      setMessages(formattedMessages);
    } catch (err) {
      // Silently fail - start with empty history
      setMessages([]);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: messages.length,
      role: 'user',
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await sendChatMessage(input, mode, userId, chatId);

      const assistantMessage: Message = {
        id: messages.length + 1,
        role: 'assistant',
        content: response.message,
        sql_query: response.sql_query,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Failed to send message:', err);
      setError('Failed to send message. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-grow overflow-hidden">
        <ChatMessageList>
          {messages.map((message) => (
            <ChatBubble
              key={message.id}
              variant={message.role === 'user' ? 'sent' : 'received'}
            >
              <ChatBubbleAvatar
                className="h-8 w-8 shrink-0"
                fallback={message.role === 'user' ? 'U' : 'AI'}
              />
              <div className="flex flex-col gap-1">
                <ChatBubbleMessage
                  variant={message.role === 'user' ? 'sent' : 'received'}
                >
                  {message.content}
                </ChatBubbleMessage>
                {message.sql_query && mode === 'admin' && (
                  <div className="text-xs text-muted-foreground font-mono bg-muted/50 p-2 rounded mt-1">
                    <strong>SQL:</strong> {message.sql_query}
                  </div>
                )}
              </div>
            </ChatBubble>
          ))}

          {isLoading && (
            <ChatBubble variant="received">
              <ChatBubbleAvatar className="h-8 w-8 shrink-0" fallback="AI" />
              <ChatBubbleMessage isLoading />
            </ChatBubble>
          )}

          {error && (
            <div className="text-sm text-destructive p-2">{error}</div>
          )}
        </ChatMessageList>
      </div>

      <div className="border-t p-4">
        <form
          onSubmit={handleSubmit}
          className="relative rounded-lg border bg-background focus-within:ring-1 focus-within:ring-ring p-1"
        >
          <ChatInput
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={
              mode === 'admin'
                ? 'Ask a question about the data...'
                : 'Type your message...'
            }
            className="min-h-12 resize-none rounded-lg bg-background border-0 p-3 shadow-none focus-visible:ring-0"
          />
          <div className="flex items-center p-3 pt-0 justify-end">
            <Button
              type="submit"
              size="sm"
              className="ml-auto gap-1.5"
              disabled={!input.trim() || isLoading}
            >
              Send
              <Send className="size-3.5" />
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

