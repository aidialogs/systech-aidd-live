"use client";

import { AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

interface DashboardErrorProps {
  error: Error;
  reset?: () => void;
}

/**
 * Error component for dashboard
 * Shows user-friendly error message with retry option
 */
export function DashboardError({ error, reset }: DashboardErrorProps) {
  return (
    <Card className="border-red-200 bg-red-50">
      <CardHeader>
        <div className="flex items-center gap-2">
          <AlertCircle className="h-5 w-5 text-red-600" />
          <CardTitle className="text-red-900">Failed to load dashboard</CardTitle>
        </div>
        <CardDescription className="text-red-700">
          {error.message || "An unexpected error occurred"}
        </CardDescription>
      </CardHeader>
      <CardContent>
        {reset && (
          <Button
            onClick={reset}
            variant="outline"
            className="border-red-300 text-red-900 hover:bg-red-100"
          >
            Try Again
          </Button>
        )}
      </CardContent>
    </Card>
  );
}
