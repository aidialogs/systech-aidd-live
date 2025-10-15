"use client"

import { Area, AreaChart, CartesianGrid, XAxis, YAxis } from "recharts"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import { Button } from "@/components/ui/button"

interface MessageChartProps {
  data: {
    time_range: "7d" | "30d";
    data_points: Array<{
      timestamp: string;
      message_count: number;
    }>;
  };
  onTimeRangeChange: (range: "7d" | "30d") => void;
}

const chartConfig = {
  messages: {
    label: "Messages",
    color: "hsl(var(--chart-1))",
  },
} satisfies ChartConfig

export function MessageChart({ data, onTimeRangeChange }: MessageChartProps) {
  // Форматирование данных для recharts
  const chartData = data.data_points.map(point => {
    const date = new Date(point.timestamp);
    return {
      date: date.toLocaleDateString('ru-RU', { 
        month: 'short', 
        day: 'numeric' 
      }),
      messages: point.message_count,
      fullDate: date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    };
  });

  return (
    <Card>
      <CardHeader>
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <CardTitle>Message Activity</CardTitle>
            <CardDescription>Total messages for the selected period</CardDescription>
          </div>
          <div className="flex gap-2">
            <Button 
              variant={data.time_range === "7d" ? "default" : "outline"}
              size="sm"
              onClick={() => onTimeRangeChange("7d")}
            >
              Last 7 days
            </Button>
            <Button 
              variant={data.time_range === "30d" ? "default" : "outline"}
              size="sm"
              onClick={() => onTimeRangeChange("30d")}
            >
              Last 30 days
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig} className="h-[300px] w-full">
          <AreaChart
            data={chartData}
            margin={{
              left: 12,
              right: 12,
              top: 12,
              bottom: 12,
            }}
          >
            <defs>
              <linearGradient id="fillMessages" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="hsl(var(--chart-1))"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="hsl(var(--chart-1))"
                  stopOpacity={0.1}
                />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis
              dataKey="date"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              minTickGap={32}
            />
            <YAxis
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              tickCount={5}
            />
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent indicator="line" />}
            />
            <Area
              type="monotone"
              dataKey="messages"
              stroke="hsl(var(--chart-1))"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#fillMessages)"
            />
          </AreaChart>
        </ChartContainer>
      </CardContent>
    </Card>
  );
}

