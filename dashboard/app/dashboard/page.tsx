"use client"

import { useState } from "react"
import { AppSidebar } from "@/components/app-sidebar"
import { ChartAreaInteractive } from "@/components/chart-area-interactive"
import { SectionCards } from "@/components/section-cards"
import { SiteHeader } from "@/components/site-header"
import { LoadingSkeleton } from "@/components/loading-skeleton"
import { ErrorMessage } from "@/components/error-message"
import { FloatingChatButton } from "@/components/floating-chat-button"
import {
  SidebarInset,
  SidebarProvider,
} from "@/components/ui/sidebar"
import { useStats } from "@/hooks/use-stats"

export default function Page() {
  const [timeRange, setTimeRange] = useState<"7d" | "30d">("7d")
  const { data, loading, error, refetch } = useStats({ timeRange })

  if (loading) {
    return <LoadingSkeleton />
  }

  if (error) {
    return <ErrorMessage error={error} onRetry={refetch} />
  }

  if (!data) {
    return null
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
        <SiteHeader />
        <div className="flex flex-1 flex-col">
          <div className="@container/main flex flex-1 flex-col gap-2">
            <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
              <SectionCards overview={data.overview} />
              <div className="px-4 lg:px-6">
                <ChartAreaInteractive
                  activity={data.message_activity}
                  onTimeRangeChange={setTimeRange}
                />
              </div>
            </div>
          </div>
        </div>
      </SidebarInset>
      <FloatingChatButton />
    </SidebarProvider>
  )
}
