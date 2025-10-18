import { ArrowRight, TrendingDown, TrendingUp } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatNumber, formatTrend } from "@/lib/formatters";

interface StatsCardProps {
  title: string;
  value: number;
  trend: number;
}

export function StatsCard({ title, value, trend }: StatsCardProps) {
  const getTrendIcon = () => {
    if (trend > 0) {
      return <TrendingUp className="size-4 text-green-500" />;
    } else if (trend < 0) {
      return <TrendingDown className="size-4 text-red-500" />;
    }
    return <ArrowRight className="size-4 text-muted-foreground" />;
  };

  const getTrendColor = () => {
    if (trend > 0) return "text-green-500";
    if (trend < 0) return "text-red-500";
    return "text-muted-foreground";
  };

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <div className="flex items-center gap-1">
          {getTrendIcon()}
          <span className={`text-xs font-medium ${getTrendColor()}`}>{formatTrend(trend)}</span>
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{formatNumber(value)}</div>
      </CardContent>
    </Card>
  );
}
