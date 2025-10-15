"use client"

import { useEffect, useState } from "react"
import { fetchStats } from "@/lib/api"
import type { StatsResponse } from "@/types/stats"

interface UseStatsOptions {
  timeRange?: "7d" | "30d"
  autoRefresh?: boolean
  refreshInterval?: number
}

interface UseStatsReturn {
  data: StatsResponse | null
  loading: boolean
  error: string | null
  refetch: () => Promise<void>
}

export function useStats(options: UseStatsOptions = {}): UseStatsReturn {
  const {
    timeRange = "7d",
    autoRefresh = false,
    refreshInterval = 30000,
  } = options

  const [data, setData] = useState<StatsResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadData = async () => {
    try {
      setError(null)
      const stats = await fetchStats(timeRange)
      setData(stats)
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to fetch statistics"
      setError(errorMessage)
      console.error("Failed to fetch stats:", err)
    } finally {
      setLoading(false)
    }
  }

  const refetch = async () => {
    setLoading(true)
    await loadData()
  }

  // Initial load
  useEffect(() => {
    loadData()
  }, [timeRange])

  // Auto-refresh
  useEffect(() => {
    if (!autoRefresh) return

    const interval = setInterval(() => {
      loadData()
    }, refreshInterval)

    return () => clearInterval(interval)
  }, [autoRefresh, refreshInterval, timeRange])

  return { data, loading, error, refetch }
}

