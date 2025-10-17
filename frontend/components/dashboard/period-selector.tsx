"use client";

import { Button } from "@/components/ui/button";
import type { Period } from "@/types/api";

interface PeriodSelectorProps {
  period: Period;
  onPeriodChange: (period: Period) => void;
}

export function PeriodSelector({ period, onPeriodChange }: PeriodSelectorProps) {
  return (
    <div className="flex gap-2">
      <Button
        variant={period === "7d" ? "default" : "outline"}
        size="sm"
        onClick={() => onPeriodChange("7d")}
      >
        Last 7 days
      </Button>
      <Button
        variant={period === "30d" ? "default" : "outline"}
        size="sm"
        onClick={() => onPeriodChange("30d")}
      >
        Last 30 days
      </Button>
    </div>
  );
}

