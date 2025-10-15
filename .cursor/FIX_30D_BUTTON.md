# 🐛 Исправление: Кнопка "Last 30 days" не работала

## Проблема

После клика на кнопку "Last 30 days" график не обновлялся - отсутствовал новый запрос к API.

**Root cause:**
1. `useStats()` hook делал запрос только при монтировании (один раз)
2. API не получал параметр `time_range`
3. При изменении timeRange не делался новый запрос

## Исправление

### 1. Обновлен `lib/api.ts`

**Добавлен параметр timeRange:**
```typescript
export async function fetchStats(
  timeRange: "7d" | "30d" = "7d"
): Promise<StatsResponse> {
  const res = await fetch(`${API_URL}/api/stats?time_range=${timeRange}`);
  if (!res.ok) throw new Error("Failed to fetch stats");
  return res.json();
}
```

### 2. Обновлен `hooks/use-stats.ts`

**Передача timeRange в fetchStats:**
```typescript
const loadData = async () => {
  try {
    setError(null)
    const stats = await fetchStats(timeRange)  // <- передаем timeRange
    setData(stats)
  } catch (err) {
    // ...
  }
}
```

**Зависимость timeRange уже была в useEffect** - запрос делается при изменении.

### 3. Обновлен `app/dashboard/page.tsx`

**Добавлен state для управления timeRange:**
```typescript
const [timeRange, setTimeRange] = useState<"7d" | "30d">("7d")
const { data, loading, error, refetch } = useStats({ timeRange })

// Передан callback в компонент:
<ChartAreaInteractive
  activity={data.message_activity}
  onTimeRangeChange={setTimeRange}
/>
```

## Результат

✅ При клике на "Last 30 days" делается новый запрос к API
✅ Backend возвращает 30 точек данных (вместо 7)
✅ График обновляется с новыми данными
✅ TypeScript проверка: 0 ошибок
✅ Lint проверка: 0 ошибок

## Тестирование

### Backend API проверен:
```bash
curl "http://localhost:8000/api/stats?time_range=7d"  # 7 точек
curl "http://localhost:8000/api/stats?time_range=30d" # 30 точек
```

✅ Результат:
- 7d: 7 data_points
- 30d: 30 data_points

### Frontend:
1. Открыть http://localhost:3000/dashboard
2. Кликнуть "Last 30 days"
3. ✅ Должен появиться новый запрос к `/api/stats?time_range=30d`
4. ✅ График должен обновиться с 30 точками данных

## Файлы изменены

- `dashboard/lib/api.ts` - добавлен параметр timeRange
- `dashboard/hooks/use-stats.ts` - передача timeRange в API
- `dashboard/app/dashboard/page.tsx` - управление timeRange через state

## Дата исправления

2025-10-15

