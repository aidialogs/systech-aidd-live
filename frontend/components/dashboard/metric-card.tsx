import { ArrowDown, ArrowUp } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

interface MetricCardProps {
  title: string;
  value: string;
  trend: string;
  description: string;
}

/**
 * Metric card component displaying key statistics
 * Shows value with trend indicator (positive/negative)
 */
export function MetricCard({ title, value, trend, description }: MetricCardProps) {
  // Determine if trend is positive or negative
  const isPositive = trend.startsWith("+");
  const isNegative = trend.startsWith("-");

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <div className="flex items-center gap-1 pt-1">
          {isPositive && <ArrowUp className="h-4 w-4 text-green-600" />}
          {isNegative && <ArrowDown className="h-4 w-4 text-red-600" />}
          <span
            className={`text-xs font-medium ${
              isPositive ? "text-green-600" : isNegative ? "text-red-600" : "text-gray-600"
            }`}
          >
            {trend}
          </span>
        </div>
        <CardDescription className="mt-1 text-xs">{description}</CardDescription>
      </CardContent>
    </Card>
  );
}
