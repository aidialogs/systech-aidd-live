'use client';

import { Code, Database } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ModeToggleProps {
  mode: 'normal' | 'admin';
  onModeChange: (mode: 'normal' | 'admin') => void;
}

export function ModeToggle({ mode, onModeChange }: ModeToggleProps) {
  return (
    <div className="inline-flex rounded-lg border p-1 bg-muted">
      <button
        onClick={() => onModeChange('normal')}
        className={cn(
          'inline-flex items-center gap-2 rounded-md px-3 py-1.5 text-sm font-medium transition-all',
          mode === 'normal'
            ? 'bg-background text-foreground shadow-sm'
            : 'text-muted-foreground hover:text-foreground'
        )}
      >
        <Code size={16} />
        Normal
      </button>
      <button
        onClick={() => onModeChange('admin')}
        className={cn(
          'inline-flex items-center gap-2 rounded-md px-3 py-1.5 text-sm font-medium transition-all',
          mode === 'admin'
            ? 'bg-background text-foreground shadow-sm'
            : 'text-muted-foreground hover:text-foreground'
        )}
      >
        <Database size={16} />
        Admin SQL
      </button>
    </div>
  );
}
