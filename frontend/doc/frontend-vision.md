# Техническое видение Frontend проекта

## 1. Технологии

### Основной стек

- **Next.js 15+** - React-фреймворк для production приложений
- **React 18+** - библиотека для построения пользовательских интерфейсов
- **TypeScript 5+** - типизированный JavaScript для надежного кода
- **shadcn/ui** - коллекция переиспользуемых компонентов на базе Radix UI
- **Tailwind CSS** - utility-first CSS фреймворк для быстрой стилизации

### Управление зависимостями

- **pnpm** - быстрый и эффективный пакетный менеджер
- **package.json** - описание проекта и зависимостей
- **pnpm-lock.yaml** - фиксация версий зависимостей

### Инструменты качества кода

- **ESLint** - статический анализ кода
- **Prettier** - автоматическое форматирование
- **TypeScript strict mode** - строгая проверка типов
- Запуск через Makefile: `make frontend-lint`, `make frontend-format`, `make frontend-type-check`
- Без pre-commit hooks - все запускается вручную

### Деплой

- **Локальный запуск** - `make frontend-dev` (порт 3000)
- **Backend API** - `make api-run` (порт 8000)
- Запуск вручную, без автоматизации CI/CD

---

## 2. Принципы разработки

### Ключевые принципы

- **KISS (Keep It Simple, Stupid)** - никакого оверинжиниринга, только необходимое
- **Компонентный подход** - переиспользуемые, изолированные компоненты
- **Server Components first** - использование React Server Components где возможно
- **Type safety** - строгая типизация TypeScript для всех компонентов

### Что НЕ используем (для простоты)

- ❌ Сложные state management решения (Redux, MobX, Zustand)
- ❌ GraphQL (используем простой REST API)
- ❌ Микрофронтенды
- ❌ Сложные дизайн-системы (создаем только необходимые компоненты)
- ❌ Server-Side Rendering для всех страниц (только где нужно)

### Что используем для качества кода

- ✅ **TypeScript strict mode** - обязательная типизация
- ✅ **React Server Components** - оптимизация производительности
- ✅ **shadcn/ui компоненты** - accessible и customizable UI
- ✅ **Tailwind CSS** - быстрая стилизация с utility классами
- ✅ **ESLint + Prettier** - консистентный стиль кода
- ✅ **App Router** - современная файловая маршрутизация Next.js

### Организация кода

- **Компоненты** - в директории `components/` (ui, dashboard, chat)
- **Утилиты** - в директории `lib/`
- **Типы** - в директории `types/`
- **API routes** - в директории `app/api/`

### Стиль кода

- Следуем **Airbnb React Style Guide** (базовые правила)
- Prettier для автоматического форматирования
- ESLint для проверки правил Next.js и TypeScript

---

## 3. Структура проекта

### Организация файлов

```
frontend/
├── app/
│   ├── layout.tsx           # Корневой layout с метаданными
│   ├── page.tsx             # Главная страница (dashboard)
│   ├── globals.css          # Глобальные стили и CSS переменные
│   ├── api/                 # API routes (опционально для проксирования)
│   └── chat/                # Страница чата (будущее)
│       └── page.tsx
├── components/
│   ├── ui/                  # shadcn/ui компоненты (button, card, etc.)
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   └── ...
│   ├── dashboard/           # Компоненты дашборда
│   │   ├── stats-card.tsx
│   │   ├── timeline-chart.tsx
│   │   └── period-selector.tsx
│   └── chat/                # Компоненты чата (будущее)
│       ├── message-list.tsx
│       └── input-box.tsx
├── lib/
│   ├── utils.ts             # Утилитарные функции (cn, formatters)
│   └── api.ts               # Функции для работы с API
├── types/
│   ├── api.ts               # TypeScript типы для API responses
│   └── dashboard.ts         # Типы для дашборда
├── public/                  # Статические файлы (favicon, images)
├── doc/                     # Документация frontend
│   ├── frontend-vision.md
│   ├── frontend-roadmap.md
│   ├── dashboard-requirements.md
│   └── sprint-f1-summary.md
├── package.json             # Зависимости и скрипты
├── tsconfig.json            # Конфигурация TypeScript
├── tailwind.config.ts       # Конфигурация Tailwind CSS
├── components.json          # Конфигурация shadcn/ui
├── next.config.js           # Конфигурация Next.js
├── .eslintrc.json           # Правила ESLint
├── .prettierrc              # Правила Prettier
└── README.md
```

### Принципы организации

- **Компонентный подход** - один компонент = один файл
- **Разделение по фичам** - dashboard/, chat/ для логических модулей
- **UI компоненты отдельно** - components/ui/ для переиспользуемых элементов
- **Минимум файлов** - только необходимое для работы

---

## 4. Архитектура приложения

### Общая схема взаимодействия

```
User (Browser)
     ↓
[Next.js App] ← Dashboard / Chat UI
     ↓
[API Client] ← fetch/axios
     ↓
[Backend API] ← FastAPI (порт 8000)
     ↓
[PostgreSQL] ← БД с данными диалогов
```

### Поток отображения данных (Dashboard)

1. Пользователь открывает главную страницу `/`
2. Dashboard компонент загружается (Server Component)
3. Вызов API: `GET /api/stats?period=7d`
4. Backend возвращает статистику и timeline
5. Отображение данных через компоненты:
   - StatsCard - метрики (пользователи, чаты, сообщения)
   - TimelineChart - график динамики сообщений
   - PeriodSelector - переключение периода (7d/30d)
6. При изменении периода - обновление через Client Component

### Компоненты архитектуры

**Next.js App Router:**

- Файловая маршрутизация в директории `app/`
- Server Components по умолчанию для оптимизации
- Client Components с `"use client"` для интерактивности
- Layouts для переиспользуемой структуры страниц

**shadcn/ui компоненты:**

- Копируются в `components/ui/` (не npm пакет)
- Полный контроль над кодом
- Построены на Radix UI primitives
- Стилизованы через Tailwind CSS

**API Client (lib/api.ts):**

- Функции для вызова backend API
- Обработка ошибок
- TypeScript типы для responses
- Базовый URL из переменных окружения

**TypeScript типы (types/):**

- Интерфейсы для API responses
- Типы для компонентов
- Enums для констант (Period: "7d" | "30d")

### Ответственность компонентов

**Dashboard (главная страница):**

- Координирует отображение всей статистики
- Управляет состоянием выбранного периода
- Загружает данные через API Client

**StatsCard:**

- Отображает одну метрику (value + trend)
- Показывает иконку тренда (↗/↘/→)
- Цветовая индикация (зеленый/красный/серый)

**TimelineChart:**

- Отображает график динамики сообщений
- Area chart с заливкой
- Адаптивный под разные размеры экрана

**PeriodSelector:**

- Client Component для интерактивности
- Переключение между 7d/30d
- Триггер перезагрузки данных

### Принципы архитектуры

- **Простота** - минимум абстракций и слоев
- **Server Components first** - оптимизация производительности
- **Type safety** - TypeScript везде
- **Accessibility** - Radix UI primitives обеспечивают доступность
- **Responsive design** - адаптивность через Tailwind breakpoints
- **Performance** - Next.js оптимизации (Image, Font, Code splitting)

---

## 5. Интеграция с Backend

### API Endpoints

Все запросы идут к FastAPI backend на `http://localhost:8000`:

**GET /api/stats?period={7d|30d}**

- Получение статистики за период
- Query параметр: `period` - "7d" или "30d"
- Response: JSON с metrics и timeline

**GET /health**

- Проверка доступности API
- Response: `{"status": "healthy"}`

### Формат данных API

```typescript
// types/api.ts
interface StatsResponse {
  metrics: {
    total_users: MetricValue;
    total_chats: MetricValue;
    total_messages: MetricValue;
    avg_message_length: MetricValue;
  };
  timeline: TimelinePoint[];
}

interface MetricValue {
  value: number;
  trend: number; // процент изменения
}

interface TimelinePoint {
  date: string; // ISO формат "2025-10-17"
  messages: number;
}
```

### API Client реализация

```typescript
// lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchStats(period: "7d" | "30d"): Promise<StatsResponse> {
  const response = await fetch(`${API_BASE_URL}/api/stats?period=${period}`);
  if (!response.ok) {
    throw new Error("Failed to fetch stats");
  }
  return response.json();
}
```

### Обработка ошибок

- **Network errors** - показываем fallback UI
- **API errors** - логируем и показываем сообщение пользователю
- **Loading states** - индикаторы загрузки через Suspense
- **Error boundaries** - ловим React ошибки

---

## 6. Работа с данными

### Стратегия загрузки данных

**Server Components (SSR/SSG):**

- Загрузка данных на сервере
- Преимущества: SEO, быстрый First Paint
- Использование: Dashboard главная страница

**Client Components (CSR):**

- Загрузка данных на клиенте
- Преимущества: интерактивность, real-time обновления
- Использование: Chat, фильтры, формы

**Кэширование:**

- Next.js автоматическое кэширование fetch запросов
- Revalidation по времени (например, каждые 60 секунд)
- Ручная инвалидация через Server Actions (если нужно)

### State Management

**Простой подход без внешних библиотек:**

- `useState` для локального состояния компонентов
- `useContext` для передачи данных между компонентами (если нужно)
- URL params для сохранения состояния фильтров
- Server state через Next.js cache

**Что НЕ используем:**

- ❌ Redux/MobX - избыточно для нашего случая
- ❌ Zustand/Jotai - простые useState достаточно
- ❌ React Query/SWR - встроенный Next.js кэш достаточен

---

## 7. Стилизация

### Подход к стилизации

**Tailwind CSS utility-first:**

```tsx
<div className="flex items-center gap-4 p-6 rounded-lg border bg-card">
  <h2 className="text-2xl font-bold">Total Users</h2>
  <span className="text-green-500">↗ +12.5%</span>
</div>
```

**CSS переменные для темизации:**

```css
/* app/globals.css */
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
}
```

**Адаптивный дизайн:**

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
  {/* Responsive grid layout */}
</div>
```

### Темная тема

- Поддержка через CSS переменные
- Переключение через `next-themes` (если нужно)
- Автоматическое определение системной темы

### Компонентный стиль

- Стили внутри компонентов (Tailwind классы)
- Переиспользуемые utility функции в `lib/utils.ts`
- Нет CSS модулей и styled-components

---

### Ограничения

- Только современные браузеры (ES2020+)
- JavaScript обязателен (не Progressive Enhancement)
- Без поддержки IE11
- Минимальное разрешение: 320px ширина

---

## 9. Подход к конфигурированию

### Переменные окружения

**Файл `.env.local` (не в git):**

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Файл `.env.example` (в git):**

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Next.js конфигурация

**next.config.js:**

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Дополнительные настройки при необходимости
};

module.exports = nextConfig;
```

### TypeScript конфигурация

**tsconfig.json:**

- Strict mode включен
- Path aliases: `@/` для удобного импорта
- Target: ES2020
- Module: ESNext

### Tailwind конфигурация

**tailwind.config.ts:**

- Кастомные цвета из shadcn/ui
- CSS переменные для темизации
- Responsive breakpoints

---

## 10. Локальный запуск

### Подготовка окружения

1. Установить Node.js 18+ (LTS версия)
2. Установить pnpm:
   ```bash
   npm install -g pnpm
   ```
3. Перейти в директорию frontend
4. Создать `.env.local` на основе `.env.example`

### Установка зависимостей

```bash
make frontend-install
```

Или напрямую:

```bash
cd frontend && pnpm install
```

### Запуск dev-сервера

```bash
make frontend-dev
```

Или напрямую:

```bash
cd frontend && pnpm dev
```

Приложение будет доступно на `http://localhost:3000`

### Запуск backend API (параллельно)

В отдельном терминале:

```bash
make api-run
```

API будет доступен на `http://localhost:8000`

### Makefile команды

```makefile
# Frontend
frontend-install      # Установка зависимостей
frontend-dev          # Запуск dev-сервера (порт 3000)
frontend-build        # Production сборка
frontend-start        # Запуск production сервера
frontend-lint         # Проверка ESLint
frontend-format       # Форматирование Prettier
frontend-type-check   # Проверка TypeScript типов
frontend-check-all    # Полная проверка (lint + types)

# Backend (для тестирования интеграции)
api-run               # Запуск API сервера (порт 8000)
api-test              # Тест API endpoints
```

### Особенности локального запуска

- Frontend работает на порту 3000 (Next.js dev server)
- Backend API работает на порту 8000 (FastAPI)
- Hot reload при изменении файлов
- Fast Refresh для React компонентов
- TypeScript проверка в реальном времени

### Деплой

Текущее состояние:

- ✅ Локальный запуск на машине разработчика
- ❌ Без production деплоя
- ❌ Без Docker контейнеризации frontend
- ❌ Без CI/CD
- ❌ Без облачных платформ (Vercel, Netlify)

Production деплой будет рассмотрен в будущих спринтах.

---

## 11. Тестирование

### Подход к тестированию

На текущем этапе (Sprint F2):

- ✅ TypeScript type checking
- ✅ ESLint проверка кода
- ✅ Prettier форматирование
- ❌ Без unit тестов (будут добавлены позже при необходимости)
- ❌ Без E2E тестов (будут добавлены позже при необходимости)

Тестирование добавляется по мере необходимости, без оверинжиниринга.

---
