'use client';

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

interface PeriodSelectorProps {
  value: 'day' | 'week' | 'month' | 'all';
  onChange: (value: 'day' | 'week' | 'month' | 'all') => void;
}

export function PeriodSelector({ value, onChange }: PeriodSelectorProps) {
  return (
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger className="w-[180px]">
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="day">Last 24 Hours</SelectItem>
        <SelectItem value="week">Last 7 Days</SelectItem>
        <SelectItem value="month">Last 30 Days</SelectItem>
        <SelectItem value="all">All Time</SelectItem>
      </SelectContent>
    </Select>
  );
}

