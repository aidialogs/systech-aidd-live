import { Card, CardContent, CardHeader } from "@/components/ui/card";

/**
 * Loading skeleton for dashboard
 * Shows placeholder cards while data is being fetched
 */
export function DashboardLoading() {
  return (
    <div className="space-y-4">
      {/* Skeleton для метрических карточек */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <Card key={i}>
            <CardHeader className="space-y-2">
              <div className="h-4 w-24 animate-pulse rounded bg-gray-200" />
              <div className="h-8 w-16 animate-pulse rounded bg-gray-200" />
            </CardHeader>
            <CardContent>
              <div className="h-3 w-32 animate-pulse rounded bg-gray-200" />
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Skeleton для графика */}
      <Card>
        <CardHeader>
          <div className="h-6 w-48 animate-pulse rounded bg-gray-200" />
        </CardHeader>
        <CardContent>
          <div className="h-64 animate-pulse rounded bg-gray-200" />
        </CardContent>
      </Card>
    </div>
  );
}
