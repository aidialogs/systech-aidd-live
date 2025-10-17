"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DashboardHeader } from "@/components/dashboard/header";
import { StatsCard } from "@/components/dashboard/stats-card";
import { PeriodSelector } from "@/components/dashboard/period-selector";
import { TimelineChart } from "@/components/dashboard/timeline-chart";
import { fetchStats } from "@/lib/api";
import type { Period, StatsResponse } from "@/types/api";

export default function DashboardPage() {
  const [period, setPeriod] = useState<Period>("7d");
  const [data, setData] = useState<StatsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadStats = async () => {
      try {
        setLoading(true);
        setError(null);
        const stats = await fetchStats(period);
        setData(stats);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch stats");
      } finally {
        setLoading(false);
      }
    };

    loadStats();
  }, [period]);

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />

      <main className="container mx-auto p-6 space-y-6">
        {loading && (
          <div className="flex items-center justify-center py-12">
            <p className="text-muted-foreground">Loading statistics...</p>
          </div>
        )}

        {error && (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <p className="text-destructive font-medium mb-2">Error loading data</p>
              <p className="text-sm text-muted-foreground">{error}</p>
              <p className="text-xs text-muted-foreground mt-2">
                Make sure the backend API is running on http://localhost:8000
              </p>
            </div>
          </div>
        )}

        {data && !loading && !error && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <StatsCard
                title="Total Users"
                value={data.metrics.total_users.value}
                trend={data.metrics.total_users.trend}
              />
              <StatsCard
                title="Active Chats"
                value={data.metrics.total_chats.value}
                trend={data.metrics.total_chats.trend}
              />
              <StatsCard
                title="Total Messages"
                value={data.metrics.total_messages.value}
                trend={data.metrics.total_messages.trend}
              />
              <StatsCard
                title="Avg Message Length"
                value={data.metrics.avg_message_length.value}
                trend={data.metrics.avg_message_length.trend}
              />
            </div>

            <Card>
              <CardHeader>
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                  <CardTitle>Messages Timeline</CardTitle>
                  <PeriodSelector period={period} onPeriodChange={setPeriod} />
                </div>
              </CardHeader>
              <CardContent>
                <TimelineChart data={data.timeline} />
              </CardContent>
            </Card>
          </>
        )}
      </main>
    </div>
  );
}

