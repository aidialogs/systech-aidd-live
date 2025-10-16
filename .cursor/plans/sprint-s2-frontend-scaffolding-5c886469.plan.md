<!-- 5c886469-c74d-413d-abfe-9dc1caef539f 51097ace-1172-42ee-be57-2c953e4004df -->
# Sprint S2: Scaffolding Frontend Проекта

## Обзор

Создание базовой инфраструктуры frontend-приложения для дашборда статистики AI-бота. Проект будет построен на современном стеке: Next.js + React + TypeScript + shadcn/ui + Tailwind CSS с использованием pnpm в качестве менеджера пакетов.

## 1. ADR для технологического стека

Создать Architecture Decision Record (ADR-07) для документирования выбора frontend технологий.

**Файл:** `/Users/akozhin/projects/systech-aidd-live/doc/adrs/ADR-07.md`

**Структура ADR:**

### Контекст

- Необходимость создания современного веб-интерфейса для дашборда статистики
- Требования к производительности, SEO и удобству разработки
- Интеграция с существующим backend API (FastAPI)

### Решение: Next.js + React + TypeScript + shadcn/ui + Tailwind CSS + pnpm

**Обоснование выбора каждого компонента:**

1. **Next.js 15** (Framework)

   - Встроенная поддержка Server-Side Rendering (SSR) и Static Site Generation (SSG)
   - App Router с React Server Components для оптимальной производительности
   - Автоматическая оптимизация (code splitting, image optimization)
   - Отличная документация и большое сообщество
   - TypeScript support из коробки

2. **React 19** (UI Library)

   - Де-факто стандарт для построения современных UI
   - Огромная экосистема компонентов и инструментов
   - Хорошо знаком LLM для генерации кода
   - Декларативный подход к построению интерфейсов

3. **TypeScript** (Type Safety)

   - Статическая типизация для предотвращения ошибок
   - Улучшенный DX с автокомплитом и IntelliSense
   - Соответствует принципу type safety из backend vision
   - Обязательные type hints (как в backend)

4. **shadcn/ui** (UI Components)

   - Не библиотека, а коллекция copy-paste компонентов
   - Полный контроль над кодом компонентов (можно модифицировать)
   - Построено на Radix UI (accessibility из коробки)
   - Стилизация через Tailwind CSS
   - Идеально подходит для дашборда (есть готовый блок dashboard-01)

5. **Tailwind CSS** (Styling)

   - Utility-first подход для быстрой разработки
   - Responsive design из коробки
   - Минимальный bundle size (tree-shaking неиспользуемых стилей)
   - Отличная интеграция с shadcn/ui
   - Быстрая итерация над дизайном

6. **pnpm** (Package Manager)

   - Значительно быстрее npm и yarn (symlink-based approach)
   - Экономия дискового пространства (content-addressable storage)
   - Строгая изоляция зависимостей (предотвращает phantom dependencies)
   - Совместимость с монорепозиториями
   - Меньше проблем с версионированием зависимостей

### Альтернативы (рассмотренные и отвергнутые)

1. **Vite + React Router** vs Next.js

   - Vite быстрее в dev mode, но требует ручной настройки SSR
   - Next.js предоставляет больше из коробки (routing, SEO, optimization)
   - Для нашего случая (dashboard с потенциальным SEO) Next.js лучше

2. **Material-UI / Ant Design** vs shadcn/ui

   - Material-UI и Ant Design - готовые библиотеки с фиксированным стилем
   - shadcn/ui дает полный контроль над компонентами и их стилями
   - Меньший bundle size с shadcn/ui
   - Легче кастомизация под дизайн проекта

3. **CSS Modules / Styled Components** vs Tailwind CSS

   - CSS Modules требуют больше boilerplate
   - Styled Components добавляют runtime overhead
   - Tailwind CSS быстрее для прототипирования и итераций

4. **npm / yarn** vs pnpm

   - npm медленнее и занимает больше места
   - yarn v1 устарел, yarn v2+ (berry) сложнее в настройке
   - pnpm современнее и эффективнее

### Последствия

**Положительные:**

- Быстрая разработка благодаря готовым компонентам shadcn/ui
- Отличная производительность с Next.js SSR/SSG
- Type safety снижает количество ошибок
- Accessibility из коробки (Radix UI)
- Хорошая документация для всех инструментов
- LLM-friendly stack (Claude хорошо знает все компоненты)

**Отрицательные:**

- Необходимость изучения Next.js App Router (новая парадигма)
- pnpm может потребовать настройки CI/CD
- Tailwind CSS требует привыкания к utility-first подходу

**Риски и митигация:**

- Риск: Breaking changes в Next.js (быстрое развитие)
  - Митигация: Фиксация версий, осторожные обновления
- Риск: shadcn/ui компоненты требуют ручного обновления
  - Митигация: Версионирование компонентов в git

## 2. Техническое видение frontend

Создать документ frontend/doc/front-vision.md по аналогии с backend vision.md

**Файл:** `/Users/akozhin/projects/systech-aidd-live/frontend/doc/front-vision.md`

**Ключевые секции:**

### 1. Технологии

- Основной стек (Next.js 15, React 19, TypeScript 5.x, pnpm 9.x)
- UI компоненты (shadcn/ui + Radix UI + Tailwind CSS 4.x)
- Charts (Recharts для графиков)
- HTTP client (native fetch API с типизацией)
- State management (React hooks + Server Components)
- Testing (Vitest + React Testing Library)

### 2. Принципы разработки

- **KISS** - простота превыше всего (как в backend)
- **Type Safety First** - строгая типизация всего кода
- **Component-First** - переиспользуемые компоненты
- **Accessibility First** - WCAG 2.1 AA compliance
- **Mobile First** - responsive design с приоритетом на мобильные устройства
- **Server Components First** - использовать RSC где возможно для производительности

### 3. Структура проекта

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Dashboard page
│   └── globals.css        # Global styles
├── components/
│   ├── ui/                # shadcn/ui components (копируются в проект)
│   ├── dashboard/         # Dashboard-specific components
│   │   ├── metric-card.tsx
│   │   └── messages-chart.tsx
│   └── layout/            # Layout components
│       ├── header.tsx
│       └── nav.tsx
├── lib/
│   ├── api.ts            # API client для backend
│   ├── utils.ts          # Utility functions
│   └── types.ts          # TypeScript types/interfaces
├── public/               # Static assets
├── doc/                  # Documentation
├── .eslintrc.json        # ESLint config
├── .prettierrc           # Prettier config
├── tailwind.config.ts    # Tailwind configuration
├── tsconfig.json         # TypeScript config
├── next.config.ts        # Next.js configuration
├── package.json          # Dependencies
└── pnpm-lock.yaml        # Lockfile

```

### 4. Архитектура

**Компонентная структура:**

- Server Components для статического контента и data fetching
- Client Components для интерактивности
- Разделение по ответственности (presentation vs container components)

**Data Fetching:**

- Server Components fetch data на сервере (оптимальная производительность)
- Клиентские запросы через typed fetch API wrapper
- Error boundaries для graceful error handling

**Типизация:**

- Строгие TypeScript interfaces для всех API responses
- Zod schema validation для runtime type checking (опционально)
- Автоматическая генерация types из OpenAPI spec (будущее улучшение)

### 5. API Integration

- Backend endpoint: `http://localhost:8000/api/stats`
- CORS уже настроен в backend для `http://localhost:3000`
- TypeScript interfaces на основе dashboard-requirements.md контракта

### 6. UX/UI принципы

- Consistency - единообразие интерфейса
- Instant Feedback - loading states, skeletons
- Error Recovery - понятные сообщения об ошибках
- Performance - < 3s Time to Interactive
- Accessibility - keyboard navigation, screen readers

### 7. Инструменты качества

- **ESLint** - статический анализ кода
- **Prettier** - форматирование кода
- **TypeScript strict mode** - максимальная типизация
- **Lighthouse CI** - мониторинг performance (будущее)

### 8. Что НЕ используем (KISS)

- ❌ Redux / Zustand (достаточно React state + Server Components)
- ❌ GraphQL (REST API достаточно для нашего случая)
- ❌ Сложные формы (нет форм в текущем scope)
- ❌ i18n (пока только английский)
- ❌ Authentication (будет добавлено позже если нужно)

## 3. Инициализация Next.js проекта

**Команды:**

```bash
cd /Users/akozhin/projects/systech-aidd-live
pnpm create next-app@latest frontend --typescript --tailwind --eslint --app --src-dir=false --import-alias="@/*"
```

**Параметры:**

- `--typescript` - TypeScript support
- `--tailwind` - Tailwind CSS
- `--eslint` - ESLint configuration
- `--app` - App Router (не Pages Router)
- `--src-dir=false` - без src директории (app/ в корне)
- `--import-alias="@/*"` - alias для импортов

**Настройка после инициализации:**

1. Обновить `package.json`:

   - Добавить scripts для dev, build, lint, format
   - Указать engine requirement для Node.js

2. Создать `.prettierrc`:
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": false,
  "tabWidth": 2,
  "printWidth": 100,
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

3. Обновить `tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2023", "DOM", "DOM.Iterable"],
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

4. Создать `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```


## 4. Настройка shadcn/ui

**Команды:**

```bash
cd frontend
pnpm dlx shadcn@latest init
```

**Настройки при инициализации:**

- Style: Default
- Base color: Slate
- CSS variables: Yes
- Tailwind config: Yes

**Добавление компонентов для dashboard:**

```bash
pnpm dlx shadcn@latest add card button badge
```

Эти компоненты будут использоваться для MetricCard в dashboard.

**Файлы которые будут созданы:**

- `components/ui/card.tsx`
- `components/ui/button.tsx`
- `components/ui/badge.tsx`
- `lib/utils.ts` (утилита cn для className merging)

## 5. Настройка инструментов разработки

### ESLint Configuration

Обновить `.eslintrc.json`:

```json
{
  "extends": [
    "next/core-web-vitals",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ],
  "rules": {
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
    "@typescript-eslint/no-explicit-any": "error",
    "prefer-const": "error"
  }
}
```

### Prettier Configuration

Установка prettier плагина для Tailwind:

```bash
pnpm add -D prettier prettier-plugin-tailwindcss
```

### Package.json Scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "format": "prettier --write \"**/*.{ts,tsx,json,md}\"",
    "type-check": "tsc --noEmit"
  }
}
```

## 6. Создание базовой структуры

### Директории

Создать следующие директории в `frontend/`:

- `components/ui/` - shadcn/ui компоненты (создается автоматически)
- `components/dashboard/` - компоненты дашборда
- `components/layout/` - layout компоненты
- `lib/` - утилиты и типы

### Базовый Layout

Создать `app/layout.tsx` с минимальной структурой:

- HTML структура
- Metadata для SEO
- Global styles
- Font configuration (Inter)

### Заглушка Dashboard Page

Создать `app/page.tsx` с заглушкой:

- "Dashboard - Coming Soon"
- Проверка что все работает

### TypeScript Types

Создать `lib/types.ts` с интерфейсами из API контракта:

```typescript
export interface MetricCard {
  title: string;
  value: string;
  trend: string;
  description: string;
}

export interface ChartDataPoint {
  date: string;
  value: number;
}

export interface DashboardStats {
  total_users: MetricCard;
  active_dialogs: MetricCard;
  total_messages: MetricCard;
  avg_message_length: MetricCard;
  messages_chart_7d: ChartDataPoint[];
  messages_chart_30d: ChartDataPoint[];
}
```

## 7. Проверка работоспособности

### Запуск dev сервера

```bash
cd frontend
pnpm dev
```

Проверить что приложение доступно на `http://localhost:3000`

### Проверка линтера

```bash
pnpm lint
```

### Проверка форматирования

```bash
pnpm format
```

### Type checking

```bash
pnpm type-check
```

## Критерии готовности (Definition of Done)

1. ✅ ADR-07 создан и документирует выбор технологий
2. ✅ front-vision.md создан с полным описанием архитектуры
3. ✅ Next.js проект инициализирован с TypeScript и Tailwind
4. ✅ shadcn/ui настроен и базовые компоненты добавлены
5. ✅ ESLint и Prettier настроены и работают
6. ✅ Структура директорий создана
7. ✅ TypeScript types для API контракта определены
8. ✅ Dev сервер запускается без ошибок
9. ✅ Все команды (lint, format, type-check) выполняются успешно
10. ✅ Заглушка dashboard page отображается в браузере

## Следующие шаги (Sprint S3)

После завершения scaffolding в Sprint S3 будет реализован полноценный dashboard:

- Компоненты MetricCard и MessagesChart
- Интеграция с MockAPI backend
- Responsive layout
- Error handling и loading states

### To-dos

- [ ] Создать ADR-07 для документирования выбора frontend технологического стека (Next.js, React, TypeScript, shadcn/ui, Tailwind CSS, pnpm)
- [ ] Создать front-vision.md с техническим видением frontend части проекта (по аналогии с backend vision.md)
- [ ] Инициализировать Next.js проект с TypeScript, Tailwind CSS, ESLint и App Router в директории frontend/
- [ ] Настроить строгий TypeScript режим в tsconfig.json (strict mode, noUncheckedIndexedAccess, noImplicitAny)
- [ ] Настроить Prettier с конфигурацией и установить prettier-plugin-tailwindcss
- [ ] Обновить ESLint конфигурацию с правилами для TypeScript и интеграцией с Prettier
- [ ] Инициализировать shadcn/ui и добавить базовые компоненты (card, button, badge)
- [ ] Создать структуру директорий (components/dashboard/, components/layout/, lib/) и базовые файлы
- [ ] Создать TypeScript типы в lib/types.ts на основе API контракта из dashboard-requirements.md
- [ ] Создать базовый app/layout.tsx с metadata, fonts и global styles
- [ ] Создать заглушку dashboard page в app/page.tsx для проверки работоспособности
- [ ] Создать .env.local с NEXT_PUBLIC_API_URL для интеграции с backend API
- [ ] Обновить package.json scripts (dev, build, lint, format, type-check)
- [ ] Проверить что dev сервер запускается, lint/format/type-check работают без ошибок