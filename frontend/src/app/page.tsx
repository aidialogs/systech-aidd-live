import { FloatingChatButton } from '@/components/chat/floating-chat-button';

export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-4">Welcome to Devil AI Assistant 😈</h1>
        <p className="text-muted-foreground mb-8">
          Click the chat button in the bottom right corner to start a conversation.
          Switch to Admin SQL mode to query the database with natural language!
        </p>
        
        <div className="space-y-4">
          <div className="border rounded-lg p-6">
            <h2 className="text-2xl font-semibold mb-2">Normal Mode</h2>
            <p className="text-muted-foreground">
              Ask questions about coding, get programming help, or discuss technical topics.
            </p>
          </div>
          
          <div className="border rounded-lg p-6">
            <h2 className="text-2xl font-semibold mb-2">Admin SQL Mode</h2>
            <p className="text-muted-foreground">
              Query the database using natural language. SQL queries are displayed with beautiful
              syntax highlighting for easy reading and debugging.
            </p>
          </div>
        </div>
      </div>

      <FloatingChatButton />
    </main>
  );
}
