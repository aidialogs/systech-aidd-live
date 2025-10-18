"use client";

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { TimelinePoint } from "@/types/api";
import { formatDateShort } from "@/lib/formatters";

interface TimelineChartProps {
  data: TimelinePoint[];
}

export function TimelineChart({ data }: TimelineChartProps) {
  // Format data for Recharts
  const chartData = data.map((point) => ({
    date: formatDateShort(point.date),
    messages: point.messages,
  }));

  return (
    <ResponsiveContainer width="100%" height={350}>
      <AreaChart data={chartData}>
        <defs>
          <linearGradient id="colorMessages" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="hsl(var(--chart-1))" stopOpacity={0.5} />
            <stop offset="95%" stopColor="hsl(var(--chart-1))" stopOpacity={0.05} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" className="stroke-muted-foreground/20" />
        <XAxis
          dataKey="date"
          className="text-xs"
          stroke="hsl(var(--muted-foreground))"
          tick={{ fill: "hsl(var(--muted-foreground))" }}
          tickLine={{ stroke: "hsl(var(--muted-foreground))" }}
        />
        <YAxis
          className="text-xs"
          stroke="hsl(var(--muted-foreground))"
          tick={{ fill: "hsl(var(--muted-foreground))" }}
          tickLine={{ stroke: "hsl(var(--muted-foreground))" }}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: "hsl(var(--card))",
            border: "2px solid hsl(var(--border))",
            borderRadius: "var(--radius)",
            boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
          }}
          labelStyle={{ color: "hsl(var(--foreground))", fontWeight: "600" }}
          itemStyle={{ color: "hsl(var(--chart-1))", fontWeight: "600" }}
        />
        <Area
          type="monotone"
          dataKey="messages"
          stroke="hsl(var(--chart-1))"
          strokeWidth={3}
          fillOpacity={1}
          fill="url(#colorMessages)"
          dot={{ fill: "hsl(var(--chart-1))", r: 4 }}
          activeDot={{
            r: 6,
            fill: "hsl(var(--chart-1))",
            stroke: "hsl(var(--background))",
            strokeWidth: 2,
          }}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
