'use client';

import { useState } from 'react';
import { ChatInterface } from '@/components/chat/chat-interface';
import { ModeToggle } from '@/components/chat/mode-toggle';

export default function ChatPage() {
  const [mode, setMode] = useState<'normal' | 'admin'>('normal');

  return (
    <div className="container mx-auto h-[calc(100vh-3.5rem)]">
      <div className="flex flex-col h-full p-4">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold">AI Chat</h1>
            <p className="text-sm text-muted-foreground">
              {mode === 'normal'
                ? 'Chat with AI assistant'
                : 'Query database with natural language'}
            </p>
          </div>
          <ModeToggle mode={mode} onModeChange={setMode} />
        </div>

        <div className="flex-grow border rounded-lg overflow-hidden bg-background">
          <ChatInterface userId={1} chatId={1} mode={mode} />
        </div>
      </div>
    </div>
  );
}
