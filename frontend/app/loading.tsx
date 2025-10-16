import { DashboardLoading } from "@/components/dashboard/dashboard-loading";

/**
 * Loading page shown during data fetching
 * Next.js automatically displays this during async operations
 */
export default function Loading() {
  return (
    <div className="flex-1 space-y-4 px-4 py-4 md:py-6 lg:px-6">
      <DashboardLoading />
    </div>
  );
}
