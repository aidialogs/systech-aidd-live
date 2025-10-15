import { IconTrendingDown, IconTrendingUp, IconMinus } from "@tabler/icons-react"

import { Badge } from "@/components/ui/badge"
import {
  Card,
  CardAction,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import type { StatsResponse } from "@/types/stats"

interface SectionCardsProps {
  overview: StatsResponse["overview"]
}

export function SectionCards({ overview }: SectionCardsProps) {
  const cards = [
    {
      title: "Total Users",
      metric: overview.total_users,
      description: "Unique users who interacted with the bot",
    },
    {
      title: "Total Conversations",
      metric: overview.total_conversations,
      description: "Active conversation threads",
    },
    {
      title: "Total Messages",
      metric: overview.total_messages,
      description: "Messages exchanged (user + assistant)",
    },
    {
      title: "Avg Conversation Length",
      metric: overview.avg_conversation_length,
      description: "Average messages per conversation",
    },
  ]

  const getTrendIcon = (direction: "up" | "down" | "neutral") => {
    switch (direction) {
      case "up":
        return <IconTrendingUp className="size-4" />
      case "down":
        return <IconTrendingDown className="size-4" />
      case "neutral":
        return <IconMinus className="size-4" />
    }
  }

  const getTrendText = (direction: "up" | "down" | "neutral") => {
    switch (direction) {
      case "up":
        return "Trending up"
      case "down":
        return "Trending down"
      case "neutral":
        return "No change"
    }
  }

  const formatValue = (value: number, isAverage: boolean) => {
    if (isAverage) {
      return value.toFixed(1)
    }
    return value.toLocaleString()
  }

  return (
    <div className="*:data-[slot=card]:from-primary/5 *:data-[slot=card]:to-card dark:*:data-[slot=card]:bg-card grid grid-cols-1 gap-4 px-4 *:data-[slot=card]:bg-gradient-to-t *:data-[slot=card]:shadow-xs lg:px-6 @xl/main:grid-cols-2 @5xl/main:grid-cols-4">
      {cards.map((card, index) => {
        const isAverage = index === 3
        const trendSign = card.metric.trend > 0 ? "+" : ""
        
        return (
          <Card key={card.title} className="@container/card">
            <CardHeader>
              <CardDescription>{card.title}</CardDescription>
              <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
                {formatValue(card.metric.value, isAverage)}
              </CardTitle>
              <CardAction>
                <Badge variant="outline">
                  {getTrendIcon(card.metric.trend_direction)}
                  {trendSign}{card.metric.trend.toFixed(1)}%
                </Badge>
              </CardAction>
            </CardHeader>
            <CardFooter className="flex-col items-start gap-1.5 text-sm">
              <div className="line-clamp-1 flex gap-2 font-medium">
                {getTrendText(card.metric.trend_direction)}{" "}
                {getTrendIcon(card.metric.trend_direction)}
              </div>
              <div className="text-muted-foreground">{card.description}</div>
            </CardFooter>
          </Card>
        )
      })}
    </div>
  )
}
