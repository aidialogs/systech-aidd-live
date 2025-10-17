'use client';

import { Send } from 'lucide-react';
import { ChatBubble, ChatBubbleMessage, ChatBubbleAvatar } from '@/components/ui/chat-bubble';
import { ChatInput } from '@/components/ui/chat-input';
import { ChatMessageList } from '@/components/ui/chat-message-list';
import { Button } from '@/components/ui/button';

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  sql_query?: string;
}

interface ChatMessagesProps {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  mode: 'normal' | 'admin';
}

interface ChatInputFormProps {
  input: string;
  setInput: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  isLoading: boolean;
  mode: 'normal' | 'admin';
}

export function ChatMessages({ messages, isLoading, error, mode }: ChatMessagesProps) {
  return (
    <ChatMessageList>
      {messages.map((message) => (
        <ChatBubble key={message.id} variant={message.role === 'user' ? 'sent' : 'received'}>
          {message.role === 'assistant' && (
            <ChatBubbleAvatar className="h-8 w-8 shrink-0" fallback="😈" />
          )}
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
          <ChatBubbleAvatar className="h-8 w-8 shrink-0" fallback="😈" />
          <ChatBubbleMessage isLoading />
        </ChatBubble>
      )}

      {error && (
        <div className="text-sm text-destructive p-2">{error}</div>
      )}
    </ChatMessageList>
  );
}

export function ChatInputForm({ input, setInput, onSubmit, isLoading, mode }: ChatInputFormProps) {
  return (
    <form
      onSubmit={onSubmit}
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
  );
}

export type { Message };

