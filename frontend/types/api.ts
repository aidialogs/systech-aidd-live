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
