import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { TopMetrics } from '@/lib/types';

interface TopMetricsCardProps {
  metrics: TopMetrics;
}

export function TopMetricsCard({ metrics }: TopMetricsCardProps) {
  const items = [
    { 
      label: 'Most Active Users', 
      value: metrics.most_active_users, 
      color: 'text-chart-1',
      emoji: '👑',
      bgColor: 'bg-purple-500/10',
    },
    { 
      label: 'Messages Today', 
      value: metrics.messages_today, 
      color: 'text-chart-2',
      emoji: '☀️',
      bgColor: 'bg-green-500/10',
    },
    { 
      label: 'Messages This Week', 
      value: metrics.messages_this_week, 
      color: 'text-chart-3',
      emoji: '📅',
      bgColor: 'bg-orange-500/10',
    },
    { 
      label: 'Messages This Month', 
      value: metrics.messages_this_month, 
      color: 'text-chart-5',
      emoji: '🗓️',
      bgColor: 'bg-pink-500/10',
    },
  ];

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center gap-2">
          <span>Quick Metrics</span>
          <span className="text-xl">⚡</span>
        </CardTitle>
        <CardDescription>Key performance indicators at a glance</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3 pb-3">
        {items.map((item, index) => (
          <div key={item.label}>
            {index > 0 && <Separator className="my-2" />}
            <div className="flex items-center justify-between gap-3">
              <div className="flex items-center gap-2">
                <div className={`flex h-8 w-8 items-center justify-center rounded-lg ${item.bgColor}`}>
                  <span className="text-lg" role="img" aria-label={item.label}>
                    {item.emoji}
                  </span>
                </div>
                <span className="text-sm font-medium text-muted-foreground">{item.label}</span>
              </div>
              <span className={`text-xl font-bold ${item.color}`}>
                {item.value.toLocaleString()}
              </span>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

