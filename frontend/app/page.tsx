import { fetchDashboardStats } from "@/lib/api";
import { getMockDashboardStats } from "@/lib/mock-data";
import { MetricCard } from "@/components/dashboard/metric-card";
import { MessagesChart } from "@/components/dashboard/messages-chart";
import { DashboardError } from "@/components/dashboard/dashboard-error";
import { DashboardHeader } from "@/components/layout/header";
import { AppSidebar } from "@/components/app-sidebar";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";

// Feature flag для переключения между mock и real API
const USE_MOCK_DATA = process.env.NEXT_PUBLIC_USE_MOCK_DATA === "true";

export default async function DashboardPage() {
  try {
    // Fetch data: mock или real API
    const stats = USE_MOCK_DATA ? getMockDashboardStats() : await fetchDashboardStats();

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
                <MessagesChart
                  data7d={stats.messages_chart_7d}
                  data30d={stats.messages_chart_30d}
                />
              </div>
            </div>
          </div>
        </SidebarInset>
      </SidebarProvider>
    );
  } catch (error) {
    // Error handling с возможностью retry
    return (
      <div className="flex min-h-screen items-center justify-center p-4">
        <DashboardError error={error instanceof Error ? error : new Error("Unknown error")} />
      </div>
    );
  }
}
