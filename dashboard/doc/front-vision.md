# Frontend Dashboard - Техническое видение

> ADR стека: @ADR-06.md  
> Правила разработки: @conventions-front.mdc  
> План разработки: @dashboard-tasklist.md

---

## 1. Описание проекта

**Название:** Dashboard для статистики Telegram бота  
**Назначение:** Визуализация метрик диалогов и активности пользователей в реальном времени  
**Целевая аудитория:** Разработчики и администраторы бота

### Основная задача

Предоставить простой и понятный интерфейс для мониторинга:
- Общей статистики использования бота
- Активности пользователей по времени
- Трендов роста или снижения метрик

---

## 2. Технологический стек

> Детальное обоснование выбора см. в **@ADR-06.md**

### Core технологии

- **Framework:** Next.js 14+ (App Router)
- **UI Components:** shadcn/ui (темная/светлая тема)
- **Package Manager:** pnpm
- **Styling:** Tailwind CSS
- **Language:** TypeScript strict mode
- **Charts:** shadcn/ui charts (recharts wrapper)
- **HTTP Client:** native fetch (Next.js)

### Обоснование (кратко)

- **Next.js**: SSR, производительность, готовность к production
- **shadcn/ui**: контроль над кодом, accessibility, темы из коробки
- **pnpm**: скорость установки, экономия места
- **TypeScript strict**: type safety, меньше багов
- **Tailwind CSS**: быстрая разработка, маленький bundle

---

## 3. Архитектура и место в репозитории

### Структура монорепозитория

```
systech-aidd-live/
├── src/              # Backend (Python/Telegram Bot)
│   ├── main.py
│   ├── api_server.py
│   └── ...
├── dashboard/        # Frontend (Next.js) ← ВОТ ТУТ
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── ...
├── doc/              # Общая документация
│   ├── adrs/        # Architecture Decision Records
│   └── ...
├── tests/            # Backend тесты
├── Makefile          # Команды для backend
└── pyproject.toml    # Backend зависимости
```

### Независимость Frontend

Frontend живет в отдельной директории `dashboard/`:

- ✅ Независимая сборка и деплой
- ✅ Собственный package.json и node_modules
- ✅ Собственный README и документация
- ✅ Связь с backend только через REST API
- ✅ Может разрабатываться параллельно с backend

---

## 4. Интеграция с Backend

### Схема взаимодействия

```
┌─────────────────────────┐
│    Telegram Bot         │  (Python, src/main.py)
│    aiogram 3.x          │
│         +               │
│   ContextManager        │  (in-memory хранилище)
│   (conversations data)  │
└───────────┬─────────────┘
            │
            │ reads data
            ↓
┌───────────────────────────┐
│      FastAPI Server       │  (Python, src/api_server.py)
│   /api/stats endpoint     │
│   + StatsCollector        │
└───────────┬───────────────┘
            │
            │ HTTP/JSON
            │ CORS: localhost
            ↓
┌───────────────────────────┐
│     Next.js Frontend      │  (TypeScript, dashboard/)
│    Dashboard UI           │
│    - Overview Cards       │
│    - Activity Graph       │
└───────────────────────────┘
```

### API контракт

**Endpoint:** `GET /api/stats`

**Request:**
- Method: GET
- Headers: нет (без авторизации в MVP)
- Query params: нет

**Response:** JSON

```json
{
  "overview": {
    "total_users": {
      "value": 150,
      "trend": 12.5,
      "trend_direction": "up"
    },
    "total_conversations": {
      "value": 234,
      "trend": -5.2,
      "trend_direction": "down"
    },
    "total_messages": {
      "value": 3420,
      "trend": 8.3,
      "trend_direction": "up"
    },
    "avg_conversation_length": {
      "value": 14.6,
      "trend": 2.1,
      "trend_direction": "up"
    }
  },
  "message_activity": {
    "time_range": "7d",
    "data_points": [
      {
        "timestamp": "2025-10-15T00:00:00Z",
        "message_count": 45
      },
      {
        "timestamp": "2025-10-16T00:00:00Z",
        "message_count": 52
      }
    ]
  }
}
```

### Конфигурация

**Environment variable:**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

- `NEXT_PUBLIC_` префикс обязателен для Next.js (доступно в browser)
- Default: `http://localhost:8000` (локальная разработка)
- Production: настраивается через environment variables

### Типизация API

**TypeScript интерфейсы** в `dashboard/types/stats.ts`:

```typescript
export interface MetricValue {
  value: number;
  trend: number;
  trend_direction: "up" | "down" | "neutral";
}

export interface StatsResponse {
  overview: {
    total_users: MetricValue;
    total_conversations: MetricValue;
    total_messages: MetricValue;
    avg_conversation_length: MetricValue;
  };
  message_activity: {
    time_range: "7d" | "30d";
    data_points: Array<{
      timestamp: string;  // ISO 8601
      message_count: number;
    }>;
  };
}
```

**Синхронизация:**
- Backend формирует JSON согласно этой структуре
- Frontend типизирует response через интерфейс
- При изменении структуры - обновляем оба места

**Валидация (опционально):**
- Можно добавить zod schema для runtime валидации
- Пока не нужно для MVP (trust backend)

---

## 5. UI/UX Принципы

### Визуальный стиль

- **Темная тема по умолчанию** (modern look)
- **Переключатель темы** в header (light/dark mode)
- **Минимализм** в стиле shadcn/ui examples
- **Чистый и современный дизайн** без излишеств

### Responsive design

- **Desktop first** (основная аудитория работает с desktop)
- Но работает на **tablet и mobile** (адаптивный layout)
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)

### Performance

- **Быстрая первая загрузка**: <2 сек (SSR + оптимизации Next.js)
- **Маленький bundle**: Tailwind purging + code splitting
- **Плавные анимации**: transitions для hover states

### Usability

- **Понятные метрики** - без перегрузки информацией
- **Четкие тренды** - стрелки вверх/вниз, проценты
- **Читаемые графики** - не перегруженные, с понятными labels

---

## 6. Компоненты Dashboard (MVP)

### Overview Cards

**4 карточки метрик в ряд:**

| Метрика | Описание |
|---------|----------|
| Total Users | Общее количество уникальных пользователей |
| Total Conversations | Общее количество активных диалогов |
| Total Messages | Общее количество сообщений (user + assistant) |
| Avg Conversation Length | Средняя длина диалога в сообщениях |

**Каждая карточка содержит:**
- Название метрики
- Значение (число)
- Тренд (процент изменения)
- Стрелка направления (↑ вверх / ↓ вниз)
- Цвет тренда (зеленый/красный)

### Message Activity Graph

**Line chart с областью:**

- **Заголовок:** "Message Activity"
- **Подзаголовок:** "Total messages for the selected period"
- **Фильтры периода:**
  - Last 7 days
  - Last 30 days
- **Оси:**
  - X: дата/время
  - Y: количество сообщений
- **Стиль:** плавная линия с градиентной заливкой

---

## 7. Архитектура для расширения

### Модульная структура компонентов

**Принцип:** Один компонент = один файл

```
components/
├── overview-cards.tsx         # MVP
├── message-chart.tsx          # MVP
├── theme-toggle.tsx           # MVP
├── top-users-table.tsx        # Готовность к добавлению
├── recent-conversations.tsx   # Готовность к добавлению
└── ui/                        # shadcn/ui примитивы
    ├── card.tsx
    ├── table.tsx
    ├── badge.tsx
    └── ...
```

### Готовность к расширению

**Легко добавить:**
- ✅ Top Users Table (топ активных пользователей)
- ✅ Recent Conversations Table (последние диалоги)
- ✅ Фильтры по периодам (date range picker)
- ✅ Экспорт данных (CSV, JSON)
- ✅ Детальная страница пользователя (routing)

**Как добавить новый компонент:**
1. Создать файл `components/new-component.tsx`
2. Добавить TypeScript интерфейс для props
3. Использовать shadcn/ui примитивы (Card, Table, Badge)
4. Импортировать в `app/page.tsx`

### Единый API клиент

**lib/api.ts:**
```typescript
// Легко расширить новыми endpoints
export async function fetchStats(): Promise<StatsResponse> { ... }
export async function fetchUserDetails(userId: number): Promise<UserDetails> { ... }
export async function fetchConversation(chatId: number): Promise<Conversation> { ... }
```

### Переиспользуемые UI компоненты

- shadcn/ui компоненты в `components/ui/`
- Можно модифицировать (копии в проекте)
- Легко добавлять новые через `pnpm dlx shadcn@latest add <component>`

---

## 8. Технические требования

### TypeScript

- **Strict mode обязателен** (`strict: true`)
- **noUncheckedIndexedAccess** для безопасности массивов
- **Типы для всех функций и props**
- **Нет any типов** (использовать unknown)

### Responsive design

- **Mobile-first utilities** Tailwind CSS
- **Breakpoints:** sm, md, lg, xl, 2xl
- **Flexible layouts:** flexbox и grid
- **Тестирование** на разных размерах экрана

### Обработка состояний

**Обязательно обрабатывать:**

1. **Loading state:**
   ```typescript
   if (isLoading) return <Skeleton />
   ```

2. **Error state:**
   ```typescript
   if (error) return <ErrorMessage error={error} />
   ```

3. **Success state:**
   ```typescript
   return <DashboardContent data={data} />
   ```

### Auto-refresh (опционально)

- **Polling каждые 30 сек** (configurable)
- **Pause on tab inactive** (document visibility API)
- **Показывать "Last updated"** timestamp

### Error boundaries

- **Graceful failures:** не ломать весь UI при ошибке компонента
- **React Error Boundaries** для изоляции ошибок
- **Fallback UI** с сообщением об ошибке

---

## 9. Ограничения MVP

### Что НЕ делаем в MVP

- ❌ **Редактирование данных** (только чтение)
- ❌ **Авторизация пользователей** (без логина)
- ❌ **Real-time updates** (используем polling вместо WebSocket)
- ❌ **Экспорт данных** (CSV, PDF)
- ❌ **Множественные страницы** (пока только Dashboard)
- ❌ **Сложные графики** (charts, heatmaps)
- ❌ **Фильтрация и поиск** (показываем все данные)
- ❌ **Персистентные настройки** (не сохраняем preferences)

### MVP включает только:

- ✅ Чтение статистики через API
- ✅ Отображение метрик с трендами
- ✅ График активности по времени
- ✅ Темная/светлая тема
- ✅ Responsive layout
- ✅ Локальный запуск

### Будущие расширения (после MVP)

1. **Авторизация** (login/password или OAuth)
2. **Real-time updates** (WebSocket)
3. **Детальные страницы** (user profile, conversation details)
4. **Фильтры** (date range, user filter)
5. **Экспорт** (CSV, JSON, PDF)
6. **Продвинутые графики** (heatmaps, pie charts)
7. **Уведомления** (alerts на аномалии)

---

## 10. Workflow разработки

### Локальная разработка

1. **Backend:** `make run-api` → `http://localhost:8000`
2. **Frontend:** `cd dashboard && pnpm dev` → `http://localhost:3000`
3. **Проверка:** открыть dashboard, увидеть метрики

### Проверка качества

```bash
cd dashboard/
pnpm type-check   # TypeScript типы
pnpm lint         # ESLint проверка
pnpm build        # Production сборка
```

### Git workflow

- **Ветки:** feature/dashboard-*, fix/dashboard-*
- **Коммиты:** понятные сообщения с префиксом "dashboard:"
- **PR:** review перед merge в main

### Документация

- **README.md** в dashboard/ - как запустить
- **Комментарии в коде** - для сложных участков
- **ADR** - для архитектурных решений

---

## 11. Критерии успеха MVP

### Функциональные

- [ ] Dashboard отображает 4 метрики с трендами
- [ ] График активности работает с фильтрами (7d/30d)
- [ ] Переключение темной/светлой темы работает
- [ ] Данные подгружаются с backend API
- [ ] Loading и error states обработаны

### Нефункциональные

- [ ] Первая загрузка < 2 сек
- [ ] Работает на desktop, tablet, mobile
- [ ] TypeScript strict без ошибок
- [ ] Lint без ошибок
- [ ] Build успешен

### Качество кода

- [ ] Все компоненты типизированы
- [ ] Один компонент = один файл
- [ ] Используется Tailwind CSS
- [ ] Нет any типов
- [ ] Следование @conventions-front.mdc

---

## 12. Ссылки

- [Next.js Documentation](https://nextjs.org/docs)
- [shadcn/ui Dashboard Example](https://ui.shadcn.com/examples/dashboard)
- [ADR-06: Технологический стек](/doc/adrs/ADR-06.md)
- [Frontend Conventions](/.cursor/rules/conventions-front.mdc)
- [Dashboard Tasklist](/doc/dashboard-tasklist.md)

