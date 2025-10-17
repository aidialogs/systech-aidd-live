'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '@/components/ui/chart';
import { Area, AreaChart, CartesianGrid, XAxis, YAxis } from 'recharts';
import { TimeSeriesPoint } from '@/lib/types';

interface MessagesOverTimeChartProps {
  data: TimeSeriesPoint[];
  period: string;
}

const chartConfig = {
  count: {
    label: 'Messages',
    color: 'hsl(var(--chart-1))',
  },
} satisfies ChartConfig;

export function MessagesOverTimeChart({ data, period }: MessagesOverTimeChartProps) {
  // Форматирование даты в зависимости от периода
  const formatDate = (dateStr: string) => {
    if (period === 'day') return dateStr.split(' ')[1] || dateStr; // Показать время
    if (period === 'all') return dateStr.substring(0, 7); // Показать YYYY-MM
    return dateStr.substring(5); // Показать MM-DD
  };

  const formattedData = data.map((point) => ({
    ...point,
    dateLabel: formatDate(point.date),
  }));

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center gap-2">
          <span>Messages Over Time</span>
          <span className="text-xl">🔥</span>
        </CardTitle>
        <CardDescription>Message count dynamics for selected period</CardDescription>
      </CardHeader>
      <CardContent className="pb-2">
        <ChartContainer config={chartConfig} className="aspect-[16/4] w-full">
          <AreaChart 
            data={formattedData} 
            margin={{ top: 10, right: 10, left: 0, bottom: 0 }}
          >
            <defs>
              {/* Огненный градиент для заливки - снизу вверх */}
              <linearGradient id="fireGradient" x1="0" y1="1" x2="0" y2="0">
                <stop offset="0%" stopColor="#FEF08A" stopOpacity={0.3} />  {/* Желтый низ */}
                <stop offset="25%" stopColor="#FCD34D" stopOpacity={0.5} /> {/* Золотой */}
                <stop offset="50%" stopColor="#FB923C" stopOpacity={0.7} /> {/* Оранжевый */}
                <stop offset="75%" stopColor="#F87171" stopOpacity={0.85} /> {/* Красно-оранжевый */}
                <stop offset="100%" stopColor="#DC2626" stopOpacity={0.95} /> {/* Красный верх */}
              </linearGradient>
              {/* Огненный градиент для линии - слева направо с мерцанием */}
              <linearGradient id="fireStroke" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="#DC2626" />   {/* Темно-красный */}
                <stop offset="25%" stopColor="#EF4444" />  {/* Красный */}
                <stop offset="50%" stopColor="#F97316" />  {/* Оранжевый */}
                <stop offset="75%" stopColor="#FB923C" />  {/* Светло-оранжевый */}
                <stop offset="100%" stopColor="#FBBF24" /> {/* Золотой */}
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="dateLabel"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              tick={{ fontSize: 12 }}
              className="fill-muted-foreground"
            />
            <YAxis 
              tickLine={false} 
              axisLine={false} 
              tickMargin={8}
              tick={{ fontSize: 12 }}
              className="fill-muted-foreground"
            />
            <ChartTooltip content={<ChartTooltipContent />} />
            <Area
              type="monotone"
              dataKey="count"
              stroke="url(#fireStroke)"
              fill="url(#fireGradient)"
              strokeWidth={4}
            />
          </AreaChart>
        </ChartContainer>
      </CardContent>
    </Card>
  );
}

