'use client';

import { useState, useEffect } from 'react';
import { getStatistics } from '@/lib/api';
import { Statistics } from '@/lib/types';
import { PeriodSelector } from '@/components/dashboard/period-selector';
import { StatsCards } from '@/components/dashboard/stats-cards';
import { MessagesOverTimeChart } from '@/components/dashboard/messages-over-time-chart';
import { MessagesByRoleChart } from '@/components/dashboard/messages-by-role-chart';
import { TopMetricsCard } from '@/components/dashboard/top-metrics-card';
import { FloatingChatButton } from '@/components/chat/floating-chat-button';

export default function DashboardPage() {
  const [period, setPeriod] = useState<'day' | 'week' | 'month' | 'all'>('month');
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        setError(null);
        const data = await getStatistics(period);
        setStatistics(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load statistics');
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [period]);

  if (loading) {
    return (
      <div className="container flex min-h-[calc(100vh-3.5rem)] items-center justify-center">
        <div className="text-center">
          <div className="text-lg font-medium">Loading statistics...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container flex min-h-[calc(100vh-3.5rem)] items-center justify-center">
        <div className="text-center">
          <div className="text-lg font-medium text-destructive">Error: {error}</div>
          <p className="mt-2 text-sm text-muted-foreground">
            Make sure the API server is running on http://localhost:8000
          </p>
        </div>
      </div>
    );
  }

  if (!statistics) {
    return null;
  }

  return (
    <>
      <div className="container mx-auto space-y-4 py-4 pb-24">
        {/* Header with period selector */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold flex items-center gap-2">
              😈 Devil dashboard
            </h1>
            <p className="text-sm text-muted-foreground">
              Dialog statistics and analytics
            </p>
          </div>
          <PeriodSelector value={period} onChange={setPeriod} />
        </div>

        {/* Stats cards */}
        <StatsCards overview={statistics.overview} />

        {/* Charts grid */}
        <div className="grid gap-4 lg:grid-cols-2">
          <div className="lg:col-span-2">
            <MessagesOverTimeChart
              data={statistics.messages_over_time}
              period={period}
            />
          </div>
          <MessagesByRoleChart data={statistics.messages_by_role} />
          <TopMetricsCard metrics={statistics.top_metrics} />
        </div>
      </div>

      <FloatingChatButton />
    </>
  );
}
