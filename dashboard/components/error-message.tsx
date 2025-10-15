import { Button } from "@/components/ui/button"
import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  SidebarInset,
  SidebarProvider,
} from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { SiteHeader } from "@/components/site-header"

interface ErrorMessageProps {
  error: string
  onRetry?: () => void
}

export function ErrorMessage({ error, onRetry }: ErrorMessageProps) {
  return (
    <SidebarProvider
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
        <div className="flex flex-1 flex-col items-center justify-center p-8">
          <Card className="w-full max-w-md">
            <CardHeader>
              <CardTitle>Failed to load data</CardTitle>
              <CardDescription className="text-destructive">
                {error}
              </CardDescription>
            </CardHeader>
            {onRetry && (
              <CardFooter>
                <Button onClick={onRetry} className="w-full">
                  Retry
                </Button>
              </CardFooter>
            )}
          </Card>
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}

