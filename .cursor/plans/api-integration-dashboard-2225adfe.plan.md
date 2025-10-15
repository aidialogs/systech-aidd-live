<!-- 2225adfe-e2ae-457d-abd7-9744afd137c3 f292d8bf-8c09-4405-8f65-4708df02e161 -->
# План: Итерация 7 - Интеграция с API

## Обзор

Подключаем frontend к реальному backend API (`/api/stats`). Заменяем все хардкоженные данные на данные из API, добавляем обработку состояний (loading, error, success) и опционально auto-refresh.

## Текущее состояние

**Backend:**

- API работает: `GET /api/stats` (mock_stats_collector.py)
- Возвращает: `overview` (4 метрики) + `message_activity` (график)
- Каждая метрика: `{value, trend, trend_direction}`

**Frontend:**

- `lib/api.ts` - функция `fetchStats()` уже реализована ✅
- `types/stats.ts` - типы соответствуют API ✅
- Компоненты используют хардкоженные данные ❌

## Что нужно сделать

### 1. Создать custom hook для загрузки данных

**Файл:** `dashboard/hooks/use-stats.ts`

```typescript
export function useStats(timeRange: "7d" | "30d", autoRefresh = false) {
  const [data, setData] = useState<StatsResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  // Load data
  // Handle errors
  // Optional: auto-refresh every 30 sec
  
  return { data, loading, error, refetch }
}
```

**Ключевые моменты:**

- Использует `fetchStats()` из `lib/api.ts`
- Обрабатывает try/catch для ошибок
- Возвращает `{ data, loading, error, refetch }`
- Опционально: `setInterval` для auto-refresh

### 2. Обновить Dashboard страницу

**Файл:** `dashboard/app/dashboard/page.tsx`

**Изменения:**

- Добавить `"use client"` директиву (нужен для hooks)
- Использовать `useStats()` hook
- Добавить обработку loading состояния (Skeleton)
- Добавить обработку error состояния (Error message)
- Передавать данные в компоненты через props
```typescript
"use client"

export default function Page() {
  const { data, loading, error } = useStats("7d")
  
  if (loading) return <LoadingSkeleton />
  if (error) return <ErrorMessage error={error} />
  if (!data) return null
  
  return (
    <SidebarProvider>
      {/* ... */}
      <SectionCards overview={data.overview} />
      <ChartAreaInteractive activity={data.message_activity} />
      {/* ... */}
    </SidebarProvider>
  )
}
```


### 3. Обновить SectionCards компонент

**Файл:** `dashboard/components/section-cards.tsx`

**Изменения:**

- Добавить props interface
- Принимать `overview` данные из API
- Отображать реальные метрики вместо хардкода
- Правильно обрабатывать trend_direction (up/down/neutral)
```typescript
interface SectionCardsProps {
  overview: StatsResponse["overview"]
}

export function SectionCards({ overview }: SectionCardsProps) {
  const cards = [
    {
      title: "Total Users",
      metric: overview.total_users,
      description: "Unique users count"
    },
    // ... остальные 3 метрики
  ]
  
  return cards.map(card => (
    <Card>
      <CardTitle>{card.metric.value}</CardTitle>
      <Badge>{card.metric.trend}%</Badge>
      {/* ... */}
    </Card>
  ))
}
```


### 4. Обновить ChartAreaInteractive компонент

**Файл:** `dashboard/components/chart-area-interactive.tsx`

**Изменения:**

- Добавить props interface
- Принимать `message_activity` данные из API
- Использовать API данные вместо хардкоженного `chartData`
- При изменении timeRange - делать новый запрос к API
```typescript
interface ChartAreaInteractiveProps {
  activity: StatsResponse["message_activity"]
  onTimeRangeChange?: (range: "7d" | "30d") => void
}

export function ChartAreaInteractive({ activity }: ChartAreaInteractiveProps) {
  // Трансформировать data_points в формат recharts
  const chartData = activity.data_points.map(point => ({
    date: point.timestamp,
    messages: point.message_count
  }))
  
  return (
    <AreaChart data={chartData}>
      <Area dataKey="messages" />
    </AreaChart>
  )
}
```


### 5. Добавить Loading и Error компоненты

**Файл:** `dashboard/components/loading-skeleton.tsx`

```typescript
export function LoadingSkeleton() {
  return (
    <div>
      <Skeleton className="h-32 w-full" /> {/* Cards */}
      <Skeleton className="h-64 w-full" /> {/* Chart */}
    </div>
  )
}
```

**Файл:** `dashboard/components/error-message.tsx`

```typescript
export function ErrorMessage({ error }: { error: string }) {
  return (
    <div className="flex items-center justify-center p-8">
      <Card>
        <CardHeader>
          <CardTitle>Failed to load data</CardTitle>
          <CardDescription>{error}</CardDescription>
        </CardHeader>
      </Card>
    </div>
  )
}
```

### 6. Обновить .env файл

**Файл:** `dashboard/.env.local` (создать если нет)

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 7. Убрать/заменить DataTable

**Проблема:** API пока не возвращает `top_users` и `recent_conversations`

**Решение (на выбор):**

- **Вариант A**: Скрыть DataTable до итерации 8
- **Вариант B**: Оставить с mock данными и комментарием "Coming soon"

**Рекомендация:** Вариант A (убрать из page.tsx)

## Обработка состояний

### Loading State

- Показывать Skeleton компоненты
- Использовать shadcn/ui Skeleton

### Error State

- Catch ошибки fetch
- Показывать понятное сообщение пользователю
- Кнопка "Retry" для повторного запроса

### Success State

- Рендерить компоненты с реальными данными

## Auto-refresh (опционально)

В `useStats()` hook:

```typescript
useEffect(() => {
  if (!autoRefresh) return
  
  const interval = setInterval(() => {
    refetch()
  }, 30000) // 30 секунд
  
  return () => clearInterval(interval)
}, [autoRefresh])
```

## Структура файлов

```
dashboard/
├── hooks/
│   └── use-stats.ts              # NEW
├── components/
│   ├── loading-skeleton.tsx      # NEW
│   ├── error-message.tsx         # NEW
│   ├── section-cards.tsx         # UPDATE (add props)
│   └── chart-area-interactive.tsx # UPDATE (add props)
├── app/
│   └── dashboard/
│       └── page.tsx               # UPDATE (use client + hook)
└── .env.local                     # NEW
```

## Критерии успеха

- [ ] Hook `useStats()` загружает данные из API
- [ ] Dashboard отображает реальные метрики из backend
- [ ] Loading состояние работает (Skeleton)
- [ ] Error состояние работает (Error message)
- [ ] График показывает реальные данные
- [ ] TypeScript типы корректны (no errors)
- [ ] Responsive design сохранен
- [ ] Auto-refresh работает (опционально)

## Тестирование

1. **Запустить backend API:**
   ```bash
   cd /Users/akozhin/projects/systech-aidd-live
   make run-api
   ```

2. **Запустить frontend:**
   ```bash
   cd dashboard
   pnpm dev
   ```

3. **Проверить:**

   - Dashboard загружается и показывает данные
   - При остановке API - показывается error
   - При перезагрузке - показывается loading
   - Метрики соответствуют API (/api/stats)
   - График отображает корректно

4. **Type check:**
   ```bash
   pnpm type-check
   ```


## Важные замечания

- API должен быть запущен (`make run-api`)
- CORS уже настроен в backend (localhost)
- DataTable временно убираем (нет данных в API)
- Следуем TypeScript strict mode
- Один компонент = один файл

## Потенциальные проблемы

1. **CORS ошибки:** проверить что backend разрешает localhost:3000
2. **API не запущен:** добавить понятное сообщение об ошибке
3. **Неправильный формат данных:** проверить типы соответствуют backend

### To-dos

- [ ] Создать custom hook use-stats.ts для загрузки данных из API
- [ ] Создать компоненты LoadingSkeleton и ErrorMessage
- [ ] Обновить dashboard/page.tsx - добавить use client, подключить hook, обработку состояний
- [ ] Обновить section-cards.tsx - добавить props, использовать реальные данные
- [ ] Обновить chart-area-interactive.tsx - добавить props, использовать API данные
- [ ] Создать .env.local с NEXT_PUBLIC_API_URL
- [ ] Протестировать полную интеграцию (backend + frontend)