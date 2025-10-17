"use client";

import { Button } from "@/components/ui/button";
import type { ChatMode } from "@/types/api";

interface ModeToggleProps {
  mode: ChatMode;
  onModeChange: (mode: ChatMode) => void;
}

export function ModeToggle({ mode, onModeChange }: ModeToggleProps) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-xs text-white/60">Mode:</span>
      <div className="flex bg-black/50 rounded-lg p-1 gap-1">
        <Button
          size="sm"
          variant={mode === "normal" ? "default" : "ghost"}
          className={`h-6 px-2 text-xs ${
            mode === "normal"
              ? "bg-white/20 text-white hover:bg-white/30"
              : "text-white/60 hover:bg-white/10 hover:text-white"
          }`}
          onClick={() => onModeChange("normal")}
        >
          Normal
        </Button>
        <Button
          size="sm"
          variant={mode === "admin" ? "default" : "ghost"}
          className={`h-6 px-2 text-xs ${
            mode === "admin"
              ? "bg-white/20 text-white hover:bg-white/30"
              : "text-white/60 hover:bg-white/10 hover:text-white"
          }`}
          onClick={() => onModeChange("admin")}
        >
          Admin
        </Button>
      </div>
    </div>
  );
}

