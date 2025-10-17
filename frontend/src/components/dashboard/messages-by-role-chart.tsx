'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '@/components/ui/chart';
import { Bar, BarChart, XAxis, YAxis, CartesianGrid, Cell } from 'recharts';
import { MessagesByRole } from '@/lib/types';

interface MessagesByRoleChartProps {
  data: MessagesByRole;
}

// Кастомная форма горы для столбцов
const MountainShape = (props: any) => {
  const { fill, x, y, width, height } = props;
  
  if (height <= 0) return null;
  
  // Высота острой вершины (треугольника)
  const peakHeight = Math.min(30, height * 0.2);
  // Основание горы (прямоугольник)
  const baseHeight = height - peakHeight;
  
  return (
    <g>
      {/* Основание горы - прямоугольник со скругленными нижними углами */}
      <rect
        x={x}
        y={y + peakHeight}
        width={width}
        height={baseHeight}
        fill={fill}
        rx={4}
        ry={4}
      />
      {/* Острая вершина - треугольник */}
      <path
        d={`
          M ${x} ${y + peakHeight}
          L ${x + width / 2} ${y}
          L ${x + width} ${y + peakHeight}
          Z
        `}
        fill={fill}
      />
      {/* Снежная шапка на вершине (более светлая) */}
      <path
        d={`
          M ${x + width * 0.3} ${y + peakHeight * 0.6}
          L ${x + width / 2} ${y}
          L ${x + width * 0.7} ${y + peakHeight * 0.6}
          Z
        `}
        fill="rgba(255, 255, 255, 0.6)"
      />
    </g>
  );
};

const chartConfig = {
  user: {
    label: 'User',
    color: 'hsl(var(--chart-2))',
  },
  assistant: {
    label: 'Assistant',
    color: 'hsl(var(--chart-3))',
  },
  system: {
    label: 'System',
    color: 'hsl(var(--chart-4))',
  },
} satisfies ChartConfig;

export function MessagesByRoleChart({ data }: MessagesByRoleChartProps) {
  const chartData = [
    { role: 'User', count: data.user, fill: 'hsl(var(--chart-2))' },
    { role: 'Assistant', count: data.assistant, fill: 'hsl(var(--chart-3))' },
    { role: 'System', count: data.system, fill: 'hsl(var(--chart-4))' },
  ];

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center gap-2">
          <span>Messages by Role</span>
          <span className="text-xl">⛰️</span>
        </CardTitle>
        <CardDescription>Distribution across user, assistant, and system</CardDescription>
      </CardHeader>
      <CardContent className="pb-2">
        <ChartContainer config={chartConfig} className="aspect-[16/6] w-full">
          <BarChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <defs>
              {/* Снежная вершина User - градиент от темно-синего к белому */}
              <linearGradient id="mountainUser" x1="0" y1="1" x2="0" y2="0">
                <stop offset="0%" stopColor="#1E3A8A" stopOpacity={0.9} />  {/* Темно-синий низ */}
                <stop offset="30%" stopColor="#3B82F6" stopOpacity={0.85} /> {/* Синий */}
                <stop offset="60%" stopColor="#60A5FA" stopOpacity={0.8} />  {/* Светло-синий */}
                <stop offset="85%" stopColor="#DBEAFE" stopOpacity={0.9} />  {/* Очень светлый */}
                <stop offset="100%" stopColor="#FFFFFF" stopOpacity={1} />   {/* Белая вершина */}
              </linearGradient>
              {/* Снежная вершина Assistant - градиент от фиолетового к белому */}
              <linearGradient id="mountainAssistant" x1="0" y1="1" x2="0" y2="0">
                <stop offset="0%" stopColor="#581C87" stopOpacity={0.9} />  {/* Темно-фиолетовый */}
                <stop offset="30%" stopColor="#7C3AED" stopOpacity={0.85} /> {/* Фиолетовый */}
                <stop offset="60%" stopColor="#A78BFA" stopOpacity={0.8} />  {/* Светло-фиолетовый */}
                <stop offset="85%" stopColor="#EDE9FE" stopOpacity={0.9} />  {/* Очень светлый */}
                <stop offset="100%" stopColor="#FFFFFF" stopOpacity={1} />   {/* Белая вершина */}
              </linearGradient>
              {/* Снежная вершина System - градиент от бирюзового к белому */}
              <linearGradient id="mountainSystem" x1="0" y1="1" x2="0" y2="0">
                <stop offset="0%" stopColor="#0E7490" stopOpacity={0.9} />  {/* Темно-бирюзовый */}
                <stop offset="30%" stopColor="#06B6D4" stopOpacity={0.85} /> {/* Бирюзовый */}
                <stop offset="60%" stopColor="#67E8F9" stopOpacity={0.8} />  {/* Светло-бирюзовый */}
                <stop offset="85%" stopColor="#CFFAFE" stopOpacity={0.9} />  {/* Очень светлый */}
                <stop offset="100%" stopColor="#FFFFFF" stopOpacity={1} />   {/* Белая вершина */}
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis 
              dataKey="role" 
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
            <Bar dataKey="count" shape={<MountainShape />}>
              {chartData.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`}
                  fill={
                    entry.role === 'User' 
                      ? 'url(#mountainUser)' 
                      : entry.role === 'Assistant' 
                        ? 'url(#mountainAssistant)' 
                        : 'url(#mountainSystem)'
                  }
                />
              ))}
            </Bar>
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  );
}

