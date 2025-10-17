'use client';

import React, { ReactNode, useState } from 'react';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ExpandableChatProps {
  size?: 'sm' | 'md' | 'lg';
  position?: 'bottom-right' | 'bottom-left';
  icon?: ReactNode;
  children: ReactNode;
}

interface ExpandableChatHeaderProps {
  children: ReactNode;
  className?: string;
}

interface ExpandableChatBodyProps {
  children: ReactNode;
  className?: string;
}

interface ExpandableChatFooterProps {
  children: ReactNode;
  className?: string;
}

export function ExpandableChat({
  size = 'md',
  position = 'bottom-right',
  icon,
  children,
}: ExpandableChatProps) {
  const [isOpen, setIsOpen] = useState(false);

  const sizeClasses = {
    sm: 'w-80 h-96',
    md: 'w-96 h-[32rem]',
    lg: 'w-[28rem] h-[36rem]',
  };

  const positionClasses = {
    'bottom-right': 'bottom-4 right-4',
    'bottom-left': 'bottom-4 left-4',
  };

  return (
    <div className={cn('fixed z-50', positionClasses[position])}>
      {/* Chat window */}
      {isOpen && (
        <div
          className={cn(
            'mb-4 rounded-lg border bg-background shadow-lg flex flex-col',
            sizeClasses[size]
          )}
        >
          {children}
        </div>
      )}

      {/* Toggle button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex h-14 w-14 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-lg transition-all hover:scale-110 hover:shadow-xl"
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
      >
        {isOpen ? <X size={24} /> : icon}
      </button>
    </div>
  );
}

export function ExpandableChatHeader({ children, className }: ExpandableChatHeaderProps) {
  return (
    <div className={cn('flex items-center justify-between border-b p-4', className)}>
      {children}
    </div>
  );
}

export function ExpandableChatBody({ children, className }: ExpandableChatBodyProps) {
  return (
    <div className={cn('flex-1 overflow-y-auto p-4', className)}>
      {children}
    </div>
  );
}

export function ExpandableChatFooter({ children, className }: ExpandableChatFooterProps) {
  return (
    <div className={cn('border-t p-4', className)}>
      {children}
    </div>
  );
}
