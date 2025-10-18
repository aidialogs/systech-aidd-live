/**
 * API client для работы с backend
 */

import type {
  Period,
  StatsResponse,
  HealthResponse,
  ChatResponse,
  ChatMessage,
  ChatMode,
} from "@/types/api";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Получение статистики за указанный период
 */
export async function fetchStats(period: Period): Promise<StatsResponse> {
  const response = await fetch(`${API_BASE_URL}/api/stats?period=${period}`);

  if (!response.ok) {
    throw new Error(`Failed to fetch stats: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Проверка здоровья API
 */
export async function fetchHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error(`Failed to fetch health: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Отправка сообщения в чат
 */
export async function sendChatMessage(
  sessionId: string,
  message: string,
  mode: ChatMode
): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/api/chat/message`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      session_id: sessionId,
      message,
      mode,
    }),
  });

  if (!response.ok) {
    throw new Error(`Failed to send message: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Получение истории чата
 */
export async function fetchChatHistory(sessionId: string): Promise<ChatMessage[]> {
  const response = await fetch(`${API_BASE_URL}/api/chat/history/${sessionId}`);

  if (!response.ok) {
    throw new Error(`Failed to fetch chat history: ${response.statusText}`);
  }

  return response.json();
}
