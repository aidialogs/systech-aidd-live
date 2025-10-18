import type {
  Period,
  StatsResponse,
  ChatResponse,
  SendMessageRequest,
  ChatMode,
} from "@/types/api";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Fetch statistics from the backend API
 */
export async function fetchStats(period: Period): Promise<StatsResponse> {
  const response = await fetch(`${API_BASE_URL}/api/stats?period=${period}`);

  if (!response.ok) {
    throw new Error(`Failed to fetch stats: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Send a chat message to the backend
 */
export async function sendChatMessage(
  sessionId: string,
  message: string,
  mode: ChatMode = "normal"
): Promise<ChatResponse> {
  const requestData: SendMessageRequest = {
    session_id: sessionId,
    message,
    mode,
  };

  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestData),
  });

  if (!response.ok) {
    throw new Error(`Failed to send message: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Fetch chat history for a session
 */
export async function fetchChatHistory(
  sessionId: string
): Promise<{ role: string; content: string }[]> {
  const response = await fetch(`${API_BASE_URL}/api/chat/history/${sessionId}`);

  if (!response.ok) {
    throw new Error(`Failed to fetch chat history: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Check backend health status
 */
export async function checkHealth(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error(`Health check failed: ${response.statusText}`);
  }

  return response.json();
}
