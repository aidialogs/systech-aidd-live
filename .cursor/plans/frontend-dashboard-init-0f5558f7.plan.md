<!-- 0f5558f7-ac67-46c9-9b0e-2c0420867637 f853247e-ef9d-4648-b04e-d8be71565b5a -->
# Frontend Dashboard Initialization Plan

## Итерация 3: Концепция Frontend и ADR

### Цель

Создать ADR для технологического стека, техническое видение frontend с архитектурой и правила разработки

### Документы для создания

#### 1. ADR-06: Выбор технологического стека Frontend

**Файл:** `doc/adrs/ADR-06.md`

**Структура:**

- Статус: Принято
- Дата: 2025-10-15
- Контекст: необходим frontend для визуализации статистики бота
- Решение: Next.js 14 + shadcn/ui + pnpm + TypeScript strict + Tailwind CSS

**Обоснование каждой технологии:**

**Next.js 14:**

- Server Components и App Router из коробки
- Производительность (автоматический code splitting, image optimization)
- SSR/SSG для быстрой загрузки
- Встроенный API Routes (не нужен для нас, но полезно для будущего)
- Большое сообщество и документация
- vs Vite+React: более полный фреймворк, готов к production

**shadcn/ui:**

- Компоненты копируются в проект (полный контроль над кодом)
- Нет vendor lock-in (можно модифицировать как угодно)
- Построен на Radix UI (accessibility из коробки)
- Tailwind CSS базируется
- Темная/светлая тема из коробки
- vs Material-UI: легче, больше контроля, современнее
- vs Chakra UI: меньше абстракций, больше гибкости

**pnpm:**

- Скорость установки (в 2-3 раза быстрее npm)
- Экономия места (content-addressable storage, ~50% меньше места)
- Строгое управление peer dependencies (меньше конфликтов)
- Монорепо поддержка (если будет расширение)
- vs npm: быстрее, экономнее
- vs yarn: современнее, активнее развивается

**TypeScript strict mode:**

- Type safety с первого дня (меньше багов в рантайме)
- Улучшенное автодополнение в IDE
- Самодокументирующийся код
- Легче рефакторинг
- noUncheckedIndexedAccess для безопасности массивов

**Tailwind CSS:**

- Utility-first подход (быстрая разработка)
- Минимум custom CSS
- Purging неиспользуемых стилей (маленький bundle)
- Responsive design из коробки
- Отлично работает с shadcn/ui

**Альтернативы:**

1. Vite + React + Material-UI + npm
2. Remix + Ant Design + yarn
3. SvelteKit + custom components

**Последствия:**

- Быстрый старт благодаря shadcn/ui
- Отличная производительность (Next.js оптимизации)
- Легко расширять и поддерживать
- Современный стек с активным развитием

#### 2. Frontend Vision Document

**Файл:** `dashboard/doc/front-vision.md`

**Содержание:**

**1. Описание проекта**

- Dashboard для статистики Telegram бота
- Визуализация метрик в реальном времени
- Целевая аудитория: разработчики/администраторы бота

**2. Технологический стек (ссылка на ADR-06)**

- Framework: Next.js 14+ (App Router)
- UI Components: shadcn/ui (темная/светлая тема)
- Package Manager: pnpm
- Styling: Tailwind CSS
- Language: TypeScript strict mode
- Charts: shadcn/ui charts (recharts wrapper)
- HTTP Client: native fetch (Next.js)

**3. Архитектура и место в репозитории**

Структура монорепозитория:

```
systech-aidd-live/
├── src/              # Backend (Python/Telegram Bot)
├── dashboard/        # Frontend (Next.js)
├── doc/              # Общая документация
├── tests/            # Backend тесты
└── Makefile          # Команды для backend
```

Frontend живет в отдельной директории `dashboard/`:

- Независимая сборка и деплой
- Собственный package.json и node_modules
- Собственный README и документация
- Связь с backend только через REST API

**4. Интеграция с Backend**

Схема взаимодействия:

```
┌─────────────────┐
│  Telegram Bot   │  (Python, src/)
│  + Context Mgr  │
└────────┬────────┘
         │
    ┌────▼─────┐
    │ FastAPI  │  (Python, src/api_server.py)
    │ REST API │
    └────┬─────┘
         │
      HTTP/JSON
         │
    ┌────▼─────┐
    │ Next.js  │  (TypeScript, dashboard/)
    │ Frontend │
    └──────────┘
```

**API контракт:**

- Endpoint: `GET /api/stats`
- Response: JSON с метриками и временными рядами
- CORS: localhost разрешен для dev
- Env var: `NEXT_PUBLIC_API_URL=http://localhost:8000`

**Типизация API:**

- TypeScript интерфейсы в `dashboard/types/stats.ts`
- Синхронизация структуры данных между backend и frontend
- Валидация ответов API (опционально через zod)

**5. UI/UX Принципы**

- Темная тема по умолчанию + переключатель на светлую
- Минимализм в стиле shadcn/ui examples
- Responsive design (desktop first, но работает на mobile)
- Быстрая загрузка (<2 сек)
- Понятные метрики без перегрузки информацией

**6. Компоненты Dashboard (MVP)**

- Overview Cards (4 метрики с трендами)
- Message Activity Graph (line chart с фильтрами 7d/30d)

**7. Архитектура для расширения**

- Модульная структура компонентов
- Каждый компонент в отдельном файле
- Готовность к добавлению: Top Users Table, Recent Conversations Table
- Единый API клиент с типизацией
- Переиспользуемые UI компоненты (Card, Table, Badge)

**8. Технические требования**

- TypeScript strict mode (обязательно)
- Responsive design
- Обработка состояний: loading, error, success
- Auto-refresh каждые 30 сек (опционально, configurable)
- Error boundaries для graceful failures

**9. Ограничения MVP**

- Только чтение данных (no CRUD)
- Без аутентификации
- Локальный запуск (production деплой позже)
- Базовая аналитика (расширение позже)
- Без real-time updates (polling вместо WebSocket)

#### 3. Frontend Conventions

**Файл:** `.cursor/rules/conventions-front.mdc`

**Структура по аналогии с conventions.mdc:**

````markdown
---
alwaysApply: true
---
# Правила разработки Frontend

> Техническое видение: @front-vision.md  
> ADR стека: @ADR-06.md  
> План разработки: @dashboard-tasklist.md

## Главные принципы

### KISS - Keep It Simple, Stupid
- Никакого оверинжиниринга
- Только необходимое для работы MVP
- Простой и понятный код
- Минимум абстракций

### Организация кода
- **Один компонент = один файл** - строгое правило
- **Модульная структура** - components/, lib/, types/
- **Минимум файлов** - только необходимое

### TypeScript
- Весь код на TypeScript
- Strict mode обязателен
- Типы для всех пропсов и функций

## Что НЕ делать

### ❌ Запрещено использовать:
- Сложные state management (Redux, MobX)
- Избыточную абстракцию и HOC
- Class components (только functional)
- any типы (использовать unknown)
- CSS-in-JS библиотеки (только Tailwind)
- Лишние зависимости

### ✅ Разрешено использовать:
- **TypeScript strict** - обязательно
- **React hooks** - для state и эффектов
- **Server Components** - где возможно
- **Tailwind CSS** - для стилизации
- **shadcn/ui** - готовые компоненты

## Стиль кода

### Компоненты
- Functional components с TypeScript
- Props через интерфейсы
- Именование: PascalCase для компонентов
- Файлы: kebab-case.tsx

Пример:
```typescript
interface OverviewCardProps {
  title: string;
  value: number;
  trend: number;
}

export function OverviewCard({ title, value, trend }: OverviewCardProps) {
  return (...)
}
````

### Типизация

- Обязательна для всех функций
- Интерфейсы для props и данных
- Типы в отдельных файлах (types/)
- Использовать современный синтаксис

### Структура файлов

```
dashboard/
├── app/              # Next.js pages
├── components/       # React компоненты
│   ├── ui/          # shadcn/ui компоненты
│   └── *.tsx        # кастомные компоненты
├── lib/             # утилиты и API клиент
├── types/           # TypeScript типы
└── public/          # статика
```

### Hooks правила

- useState для локального state
- useEffect с cleanup
- Кастомные hooks начинаются с use
- Минимум зависимостей в deps array

### API вызовы

- Через fetch в lib/api.ts
- Обработка ошибок через try/catch
- Loading states обязательны
- Error states обязательны

## Стилизация

### Tailwind CSS

- Utility classes в JSX
- Нет inline styles
- Использовать cn() для conditional classes
- Responsive префиксы (sm:, md:, lg:)

### Темная/светлая тема

- CSS переменные для цветов
- dark: префикс для темной темы
- Переключатель через next-themes

## Инструменты качества

### TypeScript

- `pnpm type-check` - проверка типов
- Strict mode в tsconfig.json
- Все ошибки должны быть исправлены

### Линтинг

- ESLint (встроен в Next.js)
- `pnpm lint` - проверка
- Следовать рекомендациям

### Форматирование

- Prettier (опционально)
- Единый стиль кода
- 2 пробела для отступов (JS/TS convention)

## Зависимости

Основные:

- Next.js 14+
- React 18+
- TypeScript 5+
- Tailwind CSS
- shadcn/ui компоненты

Dev зависимости:

- @types/node, @types/react
- eslint, eslint-config-next
- typescript

## Структура компонентов

### Один компонент = один файл

```
components/
├── overview-cards.tsx     # OverviewCards component
├── message-chart.tsx      # MessageChart component
└── theme-toggle.tsx       # ThemeToggle component
```

### Переиспользование

- Общие компоненты в components/
- UI примитивы в components/ui/
- Бизнес-логика в отдельных компонентах

## Проверка перед коммитом

- [ ] `pnpm type-check` - типы проверены
- [ ] `pnpm lint` - линтинг пройден
- [ ] `pnpm build` - сборка успешна
- [ ] Один компонент = один файл
- [ ] Все props типизированы
- [ ] Нет any типов
- [ ] Используется Tailwind CSS
- [ ] Error states обработаны
- [ ] Loading states добавлены
````

---

## Итерация 4: Инициализация проекта

### Цель
Создать Next.js проект с настроенными темами, базовой структурой и проверить качество настройки

### Шаги инициализации

1. **Создать Next.js проект**
   ```bash
   mkdir dashboard
   cd dashboard
   pnpm create next-app@latest . --typescript --tailwind --app --no-src-dir
   ```

2. **Настроить shadcn/ui**
   ```bash
   pnpm dlx shadcn@latest init
   # Выбрать: New York style, slate цвета
   ```

3. **Установить необходимые компоненты**
   ```bash
   pnpm dlx shadcn@latest add card
   pnpm dlx shadcn@latest add table
   pnpm dlx shadcn@latest add badge
   pnpm dlx shadcn@latest add button
   pnpm dlx shadcn@latest add dropdown-menu
   ```

### Структура проекта

````


dashboard/

├── doc/

│   └── front-vision.md       # Техническое видение

├── app/

│   ├── layout.tsx            # Root layout с theme provider

│   ├── page.tsx              # Dashboard page

│   └── globals.css           # Tailwind + CSS variables

├── components/

│   ├── ui/                   # shadcn/ui компоненты

│   ├── theme-toggle.tsx      # Переключатель темы

│   ├── overview-cards.tsx    # MVP: 4 метрики

│   └── message-chart.tsx     # MVP: график активности

├── lib/

│   ├── utils.ts              # cn() и утилиты

│   └── api.ts                # API клиент

├── types/

│   └── stats.ts              # TypeScript интерфейсы

├── .env.example

├── package.json

├── tsconfig.json             # Strict mode

└── README.md

````

### Файлы для создания

**`dashboard/types/stats.ts`** - TypeScript интерфейсы:
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
      timestamp: string;
      message_count: number;
    }>;
  };
}
````

**`dashboard/lib/api.ts`** - API клиент:

```typescript
import type { StatsResponse } from "@/types/stats";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchStats(): Promise<StatsResponse> {
  const res = await fetch(`${API_URL}/api/stats`);
  if (!res.ok) throw new Error("Failed to fetch stats");
  return res.json();
}
```

**`dashboard/.env.example`**:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**`dashboard/tsconfig.json`** - добавить в compilerOptions:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true
  }
}
```

**`dashboard/README.md`** - инструкции:

```markdown
# Dashboard Frontend

Статистика Telegram бота с визуализацией метрик.

## Технологии
- Next.js 14 (App Router)
- shadcn/ui + Tailwind CSS
- TypeScript strict mode
- pnpm

## Установка
pnpm install

## Конфигурация
cp .env.example .env.local
# Настроить NEXT_PUBLIC_API_URL

## Запуск
pnpm dev          # http://localhost:3000
pnpm build        # production сборка
pnpm start        # production сервер
pnpm lint         # линтинг
pnpm type-check   # проверка типов
```

### Тестирование

1. `pnpm install` - установить зависимости
2. `pnpm dev` - запустить dev сервер
3. Открыть `http://localhost:3000` - проверить стартовую страницу
4. `pnpm type-check` - проверить TypeScript
5. `pnpm lint` - проверить линтинг
6. `pnpm build` - проверить сборку
7. Проверить импорт shadcn/ui компонентов (Card, Button)
8. Проверить переключение темы (если добавлен toggle)

### Критерии готовности

- Проект Next.js инициализирован и запускается
- shadcn/ui настроен с поддержкой обеих тем
- Базовые компоненты установлены
- TypeScript strict mode работает без ошибок
- Структура папок готова к разработке
- README с инструкциями создан
- Все проверки (lint, type-check, build) проходят

### To-dos

- [ ] Создать dashboard/doc/front-vision.md с техническим видением, описанием стека, компонентов и принципов расширяемости
- [ ] Инициализировать Next.js проект в директории dashboard/ с TypeScript и Tailwind
- [ ] Настроить shadcn/ui и установить необходимые компоненты (card, table, badge, button, dropdown-menu)
- [ ] Создать types/stats.ts с TypeScript интерфейсами для API (расширяемая структура)
- [ ] Создать lib/api.ts с базовым API клиентом (fetchStats с заглушкой)
- [ ] Создать .env.example и настроить переменные окружения (NEXT_PUBLIC_API_URL)
- [ ] Настроить tsconfig.json для strict mode (strict: true, noUncheckedIndexedAccess: true)
- [ ] Создать README.md с инструкциями по установке и запуску dashboard
- [ ] Протестировать: установка зависимостей, запуск dev сервера, TypeScript компиляция