'use client';

import { FormEvent, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { cn } from '@/lib/utils';

export interface Message {
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
  onSubmit: (e: FormEvent) => void;
  isLoading: boolean;
  mode: 'normal' | 'admin';
}

export function ChatMessages({ messages, isLoading, error, mode }: ChatMessagesProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="space-y-4">
      {messages.length === 0 && (
        <div className="text-center text-muted-foreground">
          <p>No messages yet. Start a conversation!</p>
        </div>
      )}

      {messages.map((message) => (
        <div
          key={message.id}
          className={cn(
            'flex',
            message.role === 'user' ? 'justify-end' : 'justify-start'
          )}
        >
          <div
            className={cn(
              'max-w-[85%] rounded-lg px-4 py-2',
              message.role === 'user'
                ? 'bg-primary text-primary-foreground'
                : 'bg-muted'
            )}
          >
            <p className="whitespace-pre-wrap break-words">{message.content}</p>
            
            {/* SQL Query Display with Syntax Highlighting */}
            {mode === 'admin' && message.role === 'assistant' && message.sql_query && (
              <div className="mt-3 rounded-md overflow-hidden border border-border">
                <div className="bg-muted/50 px-3 py-1 text-xs font-semibold text-muted-foreground border-b border-border">
                  SQL Query
                </div>
                <SyntaxHighlighter
                  language="sql"
                  style={vscDarkPlus}
                  customStyle={{
                    margin: 0,
                    padding: '0.75rem',
                    fontSize: '0.875rem',
                    borderRadius: 0,
                  }}
                  showLineNumbers={false}
                >
                  {message.sql_query}
                </SyntaxHighlighter>
              </div>
            )}
          </div>
        </div>
      ))}

      {isLoading && (
        <div className="flex justify-start">
          <div className="bg-muted rounded-lg px-4 py-2">
            <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
          </div>
        </div>
      )}

      {error && (
        <div className="rounded-lg bg-destructive/10 border border-destructive px-4 py-2">
          <p className="text-sm text-destructive">{error}</p>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}

export function ChatInputForm({
  input,
  setInput,
  onSubmit,
  isLoading,
  mode,
}: ChatInputFormProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [input]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSubmit(e);
    }
  };

  return (
    <form onSubmit={onSubmit} className="flex gap-2">
      <textarea
        ref={textareaRef}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={
          mode === 'normal'
            ? 'Ask me anything about coding...'
            : 'Query the database with natural language...'
        }
        className="flex-1 resize-none rounded-md border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring min-h-[2.5rem] max-h-32"
        rows={1}
        disabled={isLoading}
      />
      <button
        type="submit"
        disabled={isLoading || !input.trim()}
        className="rounded-md bg-primary px-3 text-primary-foreground transition-colors hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
      >
        <Send size={18} />
      </button>
    </form>
  );
}
