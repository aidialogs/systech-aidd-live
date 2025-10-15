export interface MetricValue {
  value: number;
  trend: number;
  trend_direction: "up" | "down" | "neutral";
}

export interface StatsResponse {
  overview: {
    total_users: MetricValue;
    total_conversations: MetricValue;
    total_messages: MetricValue;
    avg_conversation_length: MetricValue;
  };
  message_activity: {
    time_range: "7d" | "30d";
    data_points: Array<{
      timestamp: string; // ISO 8601
      message_count: number;
    }>;
  };
}

