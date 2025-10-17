// API functions for chat
export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  sql_query?: string;
}

export interface ChatResponse {
  message: string;
  sql_query?: string;
}

export async function sendChatMessage(
  message: string,
  mode: 'normal' | 'admin',
  userId: number,
  conversationId: number
): Promise<ChatResponse> {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      mode,
      user_id: userId,
      conversation_id: conversationId,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to send message');
  }

  return response.json();
}

export async function getChatHistory(
  userId: number,
  conversationId: number
): Promise<ChatMessage[]> {
  const response = await fetch(
    `/api/chat/history?user_id=${userId}&conversation_id=${conversationId}`
  );

  if (!response.ok) {
    throw new Error('Failed to load chat history');
  }

  return response.json();
}
