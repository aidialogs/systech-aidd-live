import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Overview } from '@/lib/types';

interface StatsCardsProps {
  overview: Overview;
}

export function StatsCards({ overview }: StatsCardsProps) {
  const cards = [
    {
      title: 'Total Messages',
      value: overview.total_messages.toLocaleString(),
      emoji: '💬',
      bgGradient: 'bg-gradient-to-br from-purple-500/20 to-purple-600/10',
      borderColor: 'border-purple-500/30',
    },
    {
      title: 'Total Users',
      value: overview.total_users.toLocaleString(),
      emoji: '👥',
      bgGradient: 'bg-gradient-to-br from-green-500/20 to-green-600/10',
      borderColor: 'border-green-500/30',
    },
    {
      title: 'Active Chats',
      value: overview.active_chats.toLocaleString(),
      emoji: '🔥',
      bgGradient: 'bg-gradient-to-br from-orange-500/20 to-orange-600/10',
      borderColor: 'border-orange-500/30',
    },
    {
      title: 'Avg Message Length',
      value: `${overview.avg_message_length} chars`,
      emoji: '📏',
      bgGradient: 'bg-gradient-to-br from-blue-500/20 to-blue-600/10',
      borderColor: 'border-blue-500/30',
    },
  ];

  return (
    <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
      {cards.map((card) => (
        <Card key={card.title} className="relative overflow-hidden transition-all hover:shadow-lg">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-1">
            <CardTitle className="text-sm font-medium">{card.title}</CardTitle>
            <div className={`flex h-16 w-16 items-center justify-center rounded-2xl border-2 shadow-sm ${card.bgGradient} ${card.borderColor}`}>
              <span className="text-4xl" role="img" aria-label={card.title}>
                {card.emoji}
              </span>
            </div>
          </CardHeader>
          <CardContent className="pb-3">
            <div className="text-2xl font-bold">{card.value}</div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

