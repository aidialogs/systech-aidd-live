/**
 * API types for backend integration
 */

export type Period = "7d" | "30d";

export interface MetricValue {
  value: number;
  trend: number; // процент изменения (например, 12.5 для +12.5%)
}

export interface TimelinePoint {
  date: string; // ISO формат "2025-10-17"
  messages: number;
}

export interface StatsResponse {
  metrics: {
    total_users: MetricValue;
    total_chats: MetricValue;
    total_messages: MetricValue;
    avg_message_length: MetricValue;
  };
  timeline: TimelinePoint[];
}

export interface HealthResponse {
  status: "healthy" | "unhealthy";
}

// Chat types
export type ChatMode = "normal" | "admin";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  created_at: string;
  sql_query?: string; // For admin mode debug
}

export interface ChatResponse {
  message: string;
  sql_query?: string; // For admin mode
  session_id: string;
}

export interface SendMessageRequest {
  session_id: string;
  message: string;
  mode: ChatMode;
}
