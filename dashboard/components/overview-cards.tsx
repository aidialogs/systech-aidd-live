import { TrendingUp, TrendingDown, Users, MessageSquare, MessagesSquare, Activity } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import {
  Card,
  CardAction,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import type { MetricValue } from "@/types/stats"

interface OverviewCardsProps {
  data: {
    total_users: MetricValue;
    total_conversations: MetricValue;
    total_messages: MetricValue;
    avg_conversation_length: MetricValue;
  };
}

export function OverviewCards({ data }: OverviewCardsProps) {
  const metrics = [
    {
      title: "Total Users",
      value: data.total_users.value,
      trend: data.total_users.trend,
      direction: data.total_users.trend_direction,
      icon: Users,
      description: "Уникальные пользователи",
      footer: data.total_users.trend_direction === "up" ? "Trending up this month" : "Trending down this month"
    },
    {
      title: "Total Conversations",
      value: data.total_conversations.value,
      trend: data.total_conversations.trend,
      direction: data.total_conversations.trend_direction,
      icon: MessagesSquare,
      description: "Активные диалоги",
      footer: data.total_conversations.trend_direction === "up" ? "Growing engagement" : "Needs attention"
    },
    {
      title: "Total Messages",
      value: data.total_messages.value,
      trend: data.total_messages.trend,
      direction: data.total_messages.trend_direction,
      icon: MessageSquare,
      description: "Всего сообщений",
      footer: data.total_messages.trend_direction === "up" ? "Strong activity" : "Activity decreased"
    },
    {
      title: "Avg Conversation Length",
      value: data.avg_conversation_length.value.toFixed(1),
      trend: data.avg_conversation_length.trend,
      direction: data.avg_conversation_length.trend_direction,
      icon: Activity,
      description: "Сообщений на диалог",
      footer: data.avg_conversation_length.trend_direction === "up" ? "Deeper engagement" : "Shorter conversations"
    }
  ];

  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
      {metrics.map((metric) => {
        const Icon = metric.icon;
        const TrendIcon = metric.direction === "up" ? TrendingUp : TrendingDown;
        const trendColor = metric.direction === "up" ? "text-green-600 dark:text-green-500" : "text-red-600 dark:text-red-500";
        
        return (
          <Card key={metric.title} className="@container/card">
            <CardHeader>
              <CardDescription className="flex items-center gap-2">
                <Icon className="size-4" />
                {metric.title}
              </CardDescription>
              <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
                {metric.value}
              </CardTitle>
              <CardAction>
                <Badge variant="outline" className={trendColor}>
                  <TrendIcon className="size-3" />
                  {metric.trend > 0 ? "+" : ""}{metric.trend}%
                </Badge>
              </CardAction>
            </CardHeader>
            <CardFooter className="flex-col items-start gap-1.5 text-sm">
              <div className="line-clamp-1 flex gap-2 font-medium">
                {metric.footer} <TrendIcon className={`size-4 ${trendColor}`} />
              </div>
              <div className="text-muted-foreground">
                {metric.description}
              </div>
            </CardFooter>
          </Card>
        );
      })}
    </div>
  );
}

