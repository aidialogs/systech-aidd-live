'use client';

import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';

interface ModeToggleProps {
  mode: 'normal' | 'admin';
  onModeChange: (mode: 'normal' | 'admin') => void;
}

export function ModeToggle({ mode, onModeChange }: ModeToggleProps) {
  return (
    <div className="flex items-center gap-2 p-1 bg-muted rounded-lg">
      <Button
        variant={mode === 'normal' ? 'default' : 'ghost'}
        size="sm"
        onClick={() => onModeChange('normal')}
        className="h-8"
      >
        💬 Normal
      </Button>
      <Button
        variant={mode === 'admin' ? 'default' : 'ghost'}
        size="sm"
        onClick={() => onModeChange('admin')}
        className="h-8 gap-1.5"
      >
        🔧 Admin
        {mode === 'admin' && (
          <Badge variant="secondary" className="ml-1 text-[10px] px-1.5 py-0">
            SQL
          </Badge>
        )}
      </Button>
    </div>
  );
}

