import Link from "next/link";
import { Github } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme-toggle";

export function DashboardHeader() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-14 items-center justify-between px-6">
        <div className="flex items-center gap-6">
          <h1 className="text-xl font-bold">Dashboard</h1>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon" asChild>
            <Link
              href="https://github.com/aidialogs/systech-aidd/"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Github className="size-5" />
              <span className="sr-only">GitHub</span>
            </Link>
          </Button>
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}

