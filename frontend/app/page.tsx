"use client";

import { useEffect, useState } from "react";
import { fetchDashboardStats } from "@/lib/api";
import { getMockDashboardStats } from "@/lib/mock-data";
import { MetricCard } from "@/components/dashboard/metric-card";
import { MessagesChart } from "@/components/dashboard/messages-chart";
import { DashboardError } from "@/components/dashboard/dashboard-error";
import { DashboardHeader } from "@/components/layout/header";
import { AppSidebar } from "@/components/app-sidebar";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import type { DashboardStats } from "@/lib/types";

// Feature flag для переключения между mock и real API
const USE_MOCK_DATA = process.env.NEXT_PUBLIC_USE_MOCK_DATA === "true";

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadStats() {
      try {
        setLoading(true);
        setError(null);

        // Fetch data: mock или real API
        const data = USE_MOCK_DATA ? getMockDashboardStats() : await fetchDashboardStats();
        setStats(data);
      } catch (err) {
        console.error("[Dashboard] Error loading stats:", err);
        setError(err instanceof Error ? err : new Error("Unknown error"));
      } finally {
        setLoading(false);
      }
    }

    loadStats();
  }, []);

  // Loading state
  if (loading) {
    return (
      <SidebarProvider
        defaultOpen={false}
        style={
          {
            "--sidebar-width": "calc(var(--spacing) * 72)",
            "--header-height": "calc(var(--spacing) * 12)",
          } as React.CSSProperties
        }
      >
        <AppSidebar variant="inset" />
        <SidebarInset>
          <DashboardHeader />
          <div className="flex flex-1 items-center justify-center">
            <div className="text-center">
              <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]" />
              <p className="mt-4 text-sm text-muted-foreground">Loading dashboard...</p>
            </div>
          </div>
        </SidebarInset>
      </SidebarProvider>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center p-4">
        <DashboardError error={error} />
      </div>
    );
  }

  // Success state
  if (!stats) {
    return null;
  }

  return (
    <SidebarProvider
      defaultOpen={false}
      style={
        {
          "--sidebar-width": "calc(var(--spacing) * 72)",
          "--header-height": "calc(var(--spacing) * 12)",
        } as React.CSSProperties
      }
    >
      <AppSidebar variant="inset" />
      <SidebarInset>
        <DashboardHeader />
        <div className="flex flex-1 flex-col">
          <div className="@container/main flex flex-1 flex-col gap-2">
            <div className="flex flex-col gap-4 px-4 py-4 md:gap-6 md:py-6 lg:px-6">
              {/* 4 Metric Cards */}
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <MetricCard {...stats.total_users} />
                <MetricCard {...stats.active_dialogs} />
                <MetricCard {...stats.total_messages} />
                <MetricCard {...stats.avg_message_length} />
              </div>

              {/* Chart */}
              <MessagesChart data7d={stats.messages_chart_7d} data30d={stats.messages_chart_30d} />
            </div>
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
