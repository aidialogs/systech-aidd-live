"use client";

import { useState } from "react";
import { Area, AreaChart, CartesianGrid, XAxis } from "recharts";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import type { ChartDataPoint } from "@/lib/types";

interface MessagesChartProps {
  data7d: ChartDataPoint[];
  data30d: ChartDataPoint[];
}

const chartConfig = {
  messages: {
    label: "Messages",
    color: "hsl(var(--chart-1))",
  },
} satisfies ChartConfig;

/**
 * Interactive chart showing message volume over time
 * Supports switching between 7-day and 30-day periods
 */
export function MessagesChart({ data7d, data30d }: MessagesChartProps) {
  const [period, setPeriod] = useState<"7d" | "30d">("7d");

  // Select data based on period
  const chartData = period === "7d" ? data7d : data30d;

  // Transform data for Recharts (expects 'messages' key)
  const transformedData = chartData.map((point) => ({
    date: new Date(point.date).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
    }),
    messages: point.value,
  }));

  return (
    <Card>
      <CardHeader className="flex flex-col items-stretch space-y-0 border-b p-0 sm:flex-row">
        <div className="flex flex-1 flex-col justify-center gap-1 px-6 py-5 sm:py-6">
          <CardTitle>Messages Over Time</CardTitle>
          <CardDescription>
            Showing message volume for the last {period === "7d" ? "7 days" : "30 days"}
          </CardDescription>
        </div>
        <div className="flex">
          <div className="flex flex-1 flex-col justify-center gap-1 border-t px-6 py-4 text-left sm:border-t-0 sm:border-l sm:px-8 sm:py-6">
            <ToggleGroup
              type="single"
              value={period}
              onValueChange={(value) => {
                if (value) setPeriod(value as "7d" | "30d");
              }}
            >
              <ToggleGroupItem value="7d" aria-label="Last 7 days">
                7d
              </ToggleGroupItem>
              <ToggleGroupItem value="30d" aria-label="Last 30 days">
                30d
              </ToggleGroupItem>
            </ToggleGroup>
          </div>
        </div>
      </CardHeader>
      <CardContent className="px-2 sm:p-6">
        <ChartContainer config={chartConfig} className="aspect-auto h-[250px] w-full">
          <AreaChart
            data={transformedData}
            margin={{
              left: 12,
              right: 12,
            }}
          >
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="date"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              minTickGap={32}
            />
            <ChartTooltip cursor={false} content={<ChartTooltipContent indicator="line" />} />
            <Area
              dataKey="messages"
              type="natural"
              fill="var(--color-messages)"
              fillOpacity={0.4}
              stroke="var(--color-messages)"
            />
          </AreaChart>
        </ChartContainer>
      </CardContent>
    </Card>
  );
}
