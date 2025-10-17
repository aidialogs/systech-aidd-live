'use client';

import { useState, FormEvent, useEffect } from 'react';
import { MessageCircle } from 'lucide-react';
import {
  ExpandableChat,
  ExpandableChatHeader,
  ExpandableChatBody,
  ExpandableChatFooter,
} from '@/components/ui/expandable-chat';
import { ChatMessages, ChatInputForm, Message } from '@/components/chat/floating-chat-interface';
import { ModeToggle } from '@/components/chat/mode-toggle';
import { sendChatMessage, getChatHistory } from '@/lib/api';

export function FloatingChatButton() {
  const [mode, setMode] = useState<'normal' | 'admin'>('normal');
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [historyLoaded, setHistoryLoaded] = useState(false);

  // Load chat history on mount
  useEffect(() => {
    const loadHistory = async () => {
      if (historyLoaded) return; // Only load once
      
      try {
        const history = await getChatHistory(1, 1);
        const formattedMessages = history.map((msg, idx) => ({
          id: idx,
          role: msg.role as 'user' | 'assistant',
          content: msg.content,
        }));
        setMessages(formattedMessages);
        setHistoryLoaded(true);
      } catch (err) {
        // Silently fail - start with empty history
        console.log('No previous history or failed to load');
        setHistoryLoaded(true);
      }
    };

    loadHistory();
  }, [historyLoaded]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessageText = input.trim();
    setInput('');
    setIsLoading(true);
    setError(null);

    // Add user message
    const userMessage: Message = {
      id: Date.now(), // Use timestamp for unique ID
      role: 'user',
      content: userMessageText,
    };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await sendChatMessage(userMessageText, mode, 1, 1);
      const assistantMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.message,
        sql_query: response.sql_query,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ExpandableChat size="lg" position="bottom-right" icon={<MessageCircle className="text-red-500" />}>
      <ExpandableChatHeader className="flex-col gap-2">
        <div className="text-center">
          <h1 className="text-xl font-semibold">Devil AI Assistant 😈</h1>
          <p className="text-sm text-muted-foreground">
            {mode === 'normal'
              ? 'Ask me anything about coding'
              : 'Query the database with natural language'}
          </p>
        </div>
        <div className="flex justify-center">
          <ModeToggle mode={mode} onModeChange={setMode} />
        </div>
      </ExpandableChatHeader>

      <ExpandableChatBody>
        <ChatMessages
          messages={messages}
          isLoading={isLoading}
          error={error}
          mode={mode}
        />
      </ExpandableChatBody>

      <ExpandableChatFooter>
        <ChatInputForm
          input={input}
          setInput={setInput}
          onSubmit={handleSubmit}
          isLoading={isLoading}
          mode={mode}
        />
      </ExpandableChatFooter>
    </ExpandableChat>
  );
}

