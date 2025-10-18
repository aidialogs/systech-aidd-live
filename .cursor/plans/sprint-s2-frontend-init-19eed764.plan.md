<!-- 19eed764-70f8-47f7-a703-b4d245d842f3 0b960e39-bae6-45f9-b1b9-4dc791606b8f -->
# Sprint S2: Инициализация Frontend проекта

## Обновления плана согласно решениям

✅ **ADR** → в общую папку `doc/adrs/ADR-07-frontend-stack.md`

✅ **Makefile** → только корневой с `frontend-*` командами

✅ **Charts** → упомянуть в vision/ADR как предварительный выбор

✅ **Темная/светлая тема** → настроить в S2

✅ **Layout с навигацией** → создать базовый в S2

✅ **Директория styles/** → убрать из структуры

## Цель

Создать базовую структуру frontend проекта с выбранным технологическим стеком, настроить инструменты разработки и подготовить фундамент для реализации дашборда статистики.

## Референс

- **Дизайн**: shadcn UI dashboard-01 (https://ui.shadcn.com/blocks#dashboard-01)
- **Backend API**: `GET /api/v1/statistics?period={day|week|month|all}`
- **Архитектурный стиль**: Современный React/Next.js с server components

## Технологический стек

- **Framework**: Next.js 15+ (App Router)
- **Язык**: TypeScript 5+
- **UI Library**: shadcn/ui (компонентная библиотека)
- **Styling**: Tailwind CSS
- **Пакетный менеджер**: pnpm
- **Иконки**: lucide-react
- **HTTP клиент**: native fetch (Next.js)
- **State Management**: React hooks (для начала)
- **Charts (предварительно)**: shadcn/ui charts для дашборда (S3)

## Структура плана реализации

### 1. Создание концепции и ADR

**Файл**: `frontend/doc/frontend-vision.md`

Документ по аналогии с `doc/vision.md`, но для frontend. Включает:

- Технологический стек с обоснованием выбора
- Принципы разработки (компонентный подход, TypeScript-first, DRY, KISS)
- Архитектура приложения (App Router, layouts, routing, Server Components)
- Структура проекта (папки, файлы, организация)
- Подход к стилизации (Tailwind CSS + shadcn/ui + темная/светлая тема)
- Интеграция с Backend API (fetch, types, error handling)
- Инструменты разработки (ESLint, Prettier, TypeScript strict)
- Стратегия тестирования (на будущее - unit, integration, e2e)
- Сценарии работы пользователя (дашборд + чат)
- Предварительный выбор библиотеки для графиков (shadcn/ui charts)

**Файл**: `doc/adrs/ADR-07-frontend-stack.md`

ADR документ в общей папке проекта (продолжение нумерации после ADR-06):

- **Контекст**: Необходимость выбора frontend технологий для дашборда статистики и админ-чата
- **Рассмотренные варианты**:
  - Next.js 15 (App Router) vs Next.js (Pages Router) vs Remix vs Vite + React
  - TypeScript vs JavaScript
  - shadcn/ui vs Material-UI vs Chakra UI vs Ant Design
  - Tailwind CSS vs CSS Modules vs Styled Components
  - pnpm vs npm vs yarn
  - Charts (предварительно): shadcn/ui charts vs Recharts vs Chart.js vs Tremor
- **Решение**: Next.js 15 + TypeScript + shadcn/ui + Tailwind + pnpm
- **Обоснование**:
  - **Next.js App Router**: Server Components, современная архитектура, оптимизация, SEO
  - **TypeScript**: Type safety, лучший DX, соответствие backend подходу (mypy strict)
  - **shadcn/ui**: Копируемые компоненты (не npm библиотека), полный контроль, Radix UI базис, высокое качество
  - **Tailwind CSS**: Utility-first, быстрая разработка, консистентный дизайн, отличная экосистема
  - **pnpm**: Быстрее npm/yarn, экономит место (symlinks), строгая изоляция зависимостей
  - **shadcn/ui charts** (предварительно для S3): единообразие с UI компонентами, обертка над Recharts
- **Последствия**: Современный стек, требует Node.js 18+, хорошо масштабируется, минимальные зависимости
- **Дата**: 2025-10-17

### 2. Инициализация Next.js проекта

**Команды**:

```bash
cd frontend/
pnpm create next-app@latest . --typescript --tailwind --app --src-dir --import-alias "@/*"
```

**Параметры создания** (интерактивный prompt):

- TypeScript: Yes
- ESLint: Yes
- Tailwind CSS: Yes
- `src/` directory: Yes
- App Router: Yes
- Import alias: `@/*`
- Turbopack: No (пока стабильная версия webpack)

**Результат**:

- Инициализирован Next.js 15+ с App Router
- TypeScript конфигурация (`tsconfig.json`)
- Tailwind CSS настроен (`tailwind.config.ts`, `postcss.config.js`)
- ESLint настроен (`.eslintrc.json`)
- Базовая структура `src/app/`

### 3. Настройка shadcn/ui

**Установка CLI и инициализация**:

```bash
cd frontend/
pnpm dlx shadcn@latest init
```

**Параметры конфигурации** (интерактивный setup):

- Style: Default
- Base color: Slate
- CSS variables: Yes (для поддержки тем)
- Install location: `src/components/ui`

**Файлы конфигурации**:

- `components.json` - конфигурация shadcn/ui
- Обновленный `tailwind.config.ts` с темами (dark/light)
- `src/lib/utils.ts` - утилиты для className merge (cn)

**Установка базовых компонентов**:

```bash
pnpm dlx shadcn@latest add button card input label select separator
```

Эти компоненты будут использоваться на placeholder страницах и в дашборде.

### 4. Настройка структуры проекта

**Создать папки и базовые файлы**:

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx               # Root layout с темами
│   │   ├── page.tsx                 # Home/Welcome page
│   │   ├── dashboard/
│   │   │   └── page.tsx             # Dashboard placeholder
│   │   ├── chat/
│   │   │   └── page.tsx             # Chat placeholder
│   │   └── globals.css              # Global styles + Tailwind
│   ├── components/
│   │   ├── ui/                      # shadcn/ui components (auto)
│   │   ├── dashboard/               # Dashboard-specific components (S3)
│   │   ├── chat/                    # Chat-specific components (S4)
│   │   └── shared/                  # Shared components (Header, ThemeToggle)
│   ├── lib/
│   │   ├── utils.ts                 # Utility functions (from shadcn)
│   │   ├── api.ts                   # API client functions
│   │   └── types.ts                 # TypeScript types/interfaces
│   └── config/
│       └── site.ts                  # Site configuration
├── public/                          # Static assets (favicon, etc.)
├── doc/
│   ├── frontend-vision.md
│   ├── frontend-roadmap.md
│   └── plans/
│       └── s2-frontend-init-plan.md # Этот план
├── .env.local.example
├── .env.local                       # Not in git
├── .eslintrc.json
├── .gitignore
├── .prettierrc
├── .prettierignore
├── components.json
├── next.config.ts
├── package.json
├── pnpm-lock.yaml
├── postcss.config.js
├── tailwind.config.ts
├── tsconfig.json
└── README.md
```

**Важно**: Директория `src/styles/` НЕ создается (не нужна с Tailwind CSS).

### 5. Конфигурация environment variables

**Файл**: `frontend/.env.local.example`

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Файл**: `frontend/.env.local` (не в git)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Проверить**: `frontend/.gitignore` содержит `.env*.local`

### 6. Создание базовых типов и API клиента

**Файл**: `frontend/src/lib/types.ts`

TypeScript интерфейсы на основе backend API схем (`src/api/schemas.py`):

```typescript
export interface Overview {
  total_messages: number;
  total_users: number;
  active_chats: number;
  avg_message_length: number;
}

export interface MessagesByRole {
  user: number;
  assistant: number;
  system: number;
}

export interface TimeSeriesPoint {
  date: string;  // ISO format
  count: number;
}

export interface TopMetrics {
  most_active_users: number;
  messages_today: number;
  messages_this_week: number;
  messages_this_month: number;
}

export interface Statistics {
  period: 'day' | 'week' | 'month' | 'all';
  overview: Overview;
  messages_by_role: MessagesByRole;
  messages_over_time: TimeSeriesPoint[];
  top_metrics: TopMetrics;
}
```

**Файл**: `frontend/src/lib/api.ts`

API клиент для взаимодействия с backend:

```typescript
import { Statistics } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function getStatistics(
  period: 'day' | 'week' | 'month' | 'all' = 'month'
): Promise<Statistics> {
  const response = await fetch(
    `${API_URL}/api/v1/statistics?period=${period}`,
    {
      cache: 'no-store', // Disable caching for real-time data
    }
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch statistics: ${response.statusText}`);
  }

  return response.json();
}
```

### 7. Конфигурация сайта

**Файл**: `frontend/src/config/site.ts`

```typescript
export const siteConfig = {
  name: 'SYSTECH AIDD Dashboard',
  description: 'AI-powered Telegram bot statistics dashboard and admin chat',
  url: 'http://localhost:3000',
  links: {
    github: 'https://github.com/yourusername/systech-aidd-live',
  },
};
```

### 8. Создание layout с поддержкой тем

**Файл**: `frontend/src/app/layout.tsx`

Root layout с метаданными, глобальными стилями и темами:

```typescript
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { siteConfig } from '@/config/site';
import { ThemeProvider } from '@/components/theme-provider';

const inter = Inter({ subsets: ['latin', 'cyrillic'] });

export const metadata: Metadata = {
  title: {
    default: siteConfig.name,
    template: `%s | ${siteConfig.name}`,
  },
  description: siteConfig.description,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ru" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
```

**Файл**: `frontend/src/components/theme-provider.tsx`

Провайдер тем (dark/light/system):

```typescript
'use client';

import * as React from 'react';
import { ThemeProvider as NextThemesProvider } from 'next-themes';
import { type ThemeProviderProps } from 'next-themes/dist/types';

export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}
```

Установить зависимость:

```bash
pnpm add next-themes
```

**Файл**: `frontend/src/components/shared/theme-toggle.tsx`

Компонент переключателя темы:

```typescript
'use client';

import * as React from 'react';
import { Moon, Sun } from 'lucide-react';
import { useTheme } from 'next-themes';
import { Button } from '@/components/ui/button';

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}
```

### 9. Создание базовой навигации

**Файл**: `frontend/src/components/shared/header.tsx`

Простой header с навигацией и переключателем темы:

```typescript
import Link from 'next/link';
import { ThemeToggle } from './theme-toggle';
import { Button } from '@/components/ui/button';

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <span className="font-bold">SYSTECH AIDD</span>
          </Link>
          <nav className="flex items-center space-x-6 text-sm font-medium">
            <Link href="/dashboard">
              <Button variant="ghost">Dashboard</Button>
            </Link>
            <Link href="/chat">
              <Button variant="ghost">Chat</Button>
            </Link>
          </nav>
        </div>
        <div className="flex flex-1 items-center justify-end space-x-2">
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
```

**Обновить**: `frontend/src/app/layout.tsx`

Добавить Header в layout:

```typescript
import { Header } from '@/components/shared/header';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ru" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <Header />
          <main>{children}</main>
        </ThemeProvider>
      </body>
    </html>
  );
}
```

### 10. Создание placeholder страниц

**Файл**: `frontend/src/app/page.tsx`

Home page с ссылками на дашборд и чат:

```typescript
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function HomePage() {
  return (
    <div className="flex min-h-[calc(100vh-3.5rem)] items-center justify-center p-8">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>SYSTECH AIDD</CardTitle>
          <CardDescription>
            AI-powered Telegram bot analytics and admin chat
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-4">
          <Button asChild>
            <Link href="/dashboard">Open Dashboard</Link>
          </Button>
          <Button asChild variant="outline">
            <Link href="/chat">Admin Chat</Link>
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
```

**Файл**: `frontend/src/app/dashboard/page.tsx`

Placeholder для дашборда (будет реализован в S3):

```typescript
export default function DashboardPage() {
  return (
    <div className="container flex min-h-[calc(100vh-3.5rem)] items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold">Dashboard</h1>
        <p className="mt-4 text-muted-foreground">
          Statistics dashboard will be implemented in Sprint S3
        </p>
      </div>
    </div>
  );
}
```

**Файл**: `frontend/src/app/chat/page.tsx`

Placeholder для чата (будет реализован в S4):

```typescript
export default function ChatPage() {
  return (
    <div className="container flex min-h-[calc(100vh-3.5rem)] items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold">Admin Chat</h1>
        <p className="mt-4 text-muted-foreground">
          AI chat interface will be implemented in Sprint S4
        </p>
      </div>
    </div>
  );
}
```

### 11. Настройка инструментов разработки

**Обновить**: `frontend/.eslintrc.json`

Правила для TypeScript и React:

```json
{
  "extends": [
    "next/core-web-vitals",
    "next/typescript"
  ],
  "rules": {
    "@typescript-eslint/no-unused-vars": "warn",
    "@typescript-eslint/no-explicit-any": "warn"
  }
}
```

**Создать**: `frontend/.prettierrc`

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 80,
  "arrowParens": "always"
}
```

**Создать**: `frontend/.prettierignore`

```
node_modules
.next
out
build
dist
```

**Обновить**: `frontend/package.json`

Добавить scripts:

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "lint:fix": "next lint --fix",
    "format": "prettier --write \"src/**/*.{ts,tsx,js,jsx,json,css,md}\"",
    "format:check": "prettier --check \"src/**/*.{ts,tsx,js,jsx,json,css,md}\"",
    "type-check": "tsc --noEmit"
  }
}
```

Установить Prettier:

```bash
pnpm add -D prettier
```

### 12. Настройка Next.js конфигурации

**Обновить**: `frontend/next.config.ts`

```typescript
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  
  // API proxy to backend (optional, for development)
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
};

export default nextConfig;
```

Это позволит делать запросы к `/api/v1/statistics` вместо полного URL.

### 13. Создание Makefile команд

**Обновить корневой**: `Makefile`

Добавить секцию для frontend (единственный вариант - корневой Makefile):

```makefile
# ============================================================================
# Frontend commands
# ============================================================================

.PHONY: frontend-install frontend-dev frontend-build frontend-start frontend-lint frontend-lint-fix frontend-format frontend-format-check frontend-type-check frontend-check-all

frontend-install:
	@echo "Installing frontend dependencies..."
	cd frontend && pnpm install

frontend-dev:
	@echo "Starting frontend development server..."
	cd frontend && pnpm dev

frontend-build:
	@echo "Building frontend for production..."
	cd frontend && pnpm build

frontend-start:
	@echo "Starting frontend production server..."
	cd frontend && pnpm start

frontend-lint:
	@echo "Linting frontend code..."
	cd frontend && pnpm lint

frontend-lint-fix:
	@echo "Fixing frontend linting issues..."
	cd frontend && pnpm lint:fix

frontend-format:
	@echo "Formatting frontend code..."
	cd frontend && pnpm format

frontend-format-check:
	@echo "Checking frontend code formatting..."
	cd frontend && pnpm format:check

frontend-type-check:
	@echo "Type checking frontend code..."
	cd frontend && pnpm type-check

frontend-check-all: frontend-lint frontend-format-check frontend-type-check
	@echo "✅ All frontend checks passed!"
```

### 14. Создание frontend README

**Файл**: `frontend/README.md`

```markdown
# SYSTECH AIDD Frontend

Modern web dashboard and admin chat interface for AI-powered Telegram bot analytics.

## Tech Stack

- **Framework**: Next.js 15+ (App Router)
- **Language**: TypeScript 5+
- **UI Library**: shadcn/ui
- **Styling**: Tailwind CSS
- **Package Manager**: pnpm
- **Icons**: lucide-react
- **Themes**: next-themes (dark/light/system)

## Getting Started

### Prerequisites

- Node.js 18+
- pnpm 8+

### Installation

\`\`\`bash
pnpm install
\`\`\`

### Development

\`\`\`bash
pnpm dev
\`\`\`

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

\`\`\`bash
pnpm build
pnpm start
\`\`\`

### Code Quality

\`\`\`bash
pnpm lint           # Run ESLint
pnpm format         # Format with Prettier
pnpm type-check     # TypeScript type checking
\`\`\`

## Project Structure

\`\`\`
src/
├── app/              # Next.js App Router pages
├── components/
│   ├── ui/           # shadcn/ui components
│   ├── dashboard/    # Dashboard components
│   ├── chat/         # Chat components
│   └── shared/       # Shared components (Header, ThemeToggle)
├── lib/              # Utilities and helpers
│   ├── api.ts        # API client
│   ├── types.ts      # TypeScript types
│   └── utils.ts      # Utility functions
└── config/           # Configuration
    └── site.ts       # Site config
\`\`\`

## Environment Variables

Copy \`.env.local.example\` to \`.env.local\`:

\`\`\`bash
NEXT_PUBLIC_API_URL=http://localhost:8000
\`\`\`

## Features

- 📊 **Dashboard**: Real-time statistics and analytics (Sprint S3)
- 💬 **Admin Chat**: AI-powered chat interface (Sprint S4)
- 🎨 **Modern UI**: Built with shadcn/ui and Tailwind CSS
- 🌓 **Dark Mode**: Light/Dark/System theme support
- 📱 **Responsive**: Mobile-friendly design
- ⚡ **Fast**: Next.js App Router with Server Components

## Documentation

- [Frontend Vision](doc/frontend-vision.md)
- [Frontend Roadmap](doc/frontend-roadmap.md)
- [Sprint Plans](doc/plans/)

## Backend API

Backend API runs on \`http://localhost:8000\`:

- \`GET /api/v1/statistics?period={day|week|month|all}\` - Statistics data

See [API examples](../doc/api-examples.md) for details.
```

### 15. Обновить документацию проекта

**Обновить**: `frontend/doc/frontend-roadmap.md`

- Обновить статус спринта S2 на "✅ Completed"
- Добавить ссылку на план в таблицу: `[s2-frontend-init-plan.md](plans/s2-frontend-init-plan.md)`
- Указать дату завершения

**Обновить корневой**: `README.md`

Добавить секцию про frontend:

```markdown
## 🎨 Frontend Dashboard

Modern web interface for statistics dashboard and admin chat.

### Tech Stack

- Next.js 15 (App Router) + TypeScript + shadcn/ui + Tailwind CSS

### Quick Start

\`\`\`bash
# Install frontend dependencies
make frontend-install

# Start development server
make frontend-dev

# Open http://localhost:3000
\`\`\`

### Commands

\`\`\`bash
make frontend-dev            # Start dev server
make frontend-build          # Production build
make frontend-lint           # Lint code
make frontend-format         # Format code
make frontend-type-check     # TypeScript check
make frontend-check-all      # All checks
\`\`\`

See [frontend/README.md](frontend/README.md) for details.
```

### 16. Финальная проверка и тестирование

**Проверить работоспособность**:

1. ✅ Backend API работает (`make api-run`)
2. ✅ Frontend запускается (`make frontend-dev`)
3. ✅ Нет ошибок TypeScript (`make frontend-type-check`)
4. ✅ Нет ошибок ESLint (`make frontend-lint`)
5. ✅ Prettier форматирование корректно (`make frontend-format-check`)
6. ✅ Переключатель темы работает (light/dark/system)
7. ✅ Навигация работает (header с ссылками)
8. ✅ Страницы открываются:

   - http://localhost:3000 (home с карточкой)
   - http://localhost:3000/dashboard (placeholder)
   - http://localhost:3000/chat (placeholder)

**Проверить интеграцию**:

1. ✅ API клиент (`src/lib/api.ts`) может получить данные от backend
2. ✅ Environment variables загружаются корректно
3. ✅ shadcn/ui компоненты работают (Button, Card)
4. ✅ Темы переключаются без ошибок

## Критерии успеха

- ✅ Next.js проект инициализирован с TypeScript и App Router
- ✅ shadcn/ui установлен и настроен с базовыми компонентами
- ✅ Tailwind CSS работает корректно
- ✅ pnpm используется как пакетный менеджер
- ✅ Структура проекта создана и документирована
- ✅ API клиент готов для интеграции с backend
- ✅ TypeScript типы соответствуют backend схемам
- ✅ Environment variables настроены
- ✅ Инструменты разработки (ESLint, Prettier) работают
- ✅ Makefile команды созданы и протестированы (только корневой)
- ✅ Placeholder страницы созданы (/, /dashboard, /chat)
- ✅ Header с навигацией создан
- ✅ Темная/светлая тема работает (next-themes)
- ✅ Frontend README документация создана
- ✅ Frontend vision документ создан
- ✅ ADR-07 создан в общей папке `doc/adrs/`
- ✅ Проект готов к реализации дашборда (Sprint S3)
- ✅ Нет TypeScript/ESLint/Prettier ошибок
- ✅ Dev server запускается без ошибок

## Файловая структура после выполнения

```
systech-aidd-live/
├── frontend/                        # Новая директория
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx           # С ThemeProvider
│   │   │   ├── page.tsx
│   │   │   ├── dashboard/page.tsx
│   │   │   ├── chat/page.tsx
│   │   │   └── globals.css
│   │   ├── components/
│   │   │   ├── ui/                  # shadcn/ui компоненты
│   │   │   ├── dashboard/           # Пустая (для S3)
│   │   │   ├── chat/                # Пустая (для S4)
│   │   │   ├── shared/
│   │   │   │   ├── header.tsx       # Навигация
│   │   │   │   └── theme-toggle.tsx # Переключатель темы
│   │   │   └── theme-provider.tsx
│   │   ├── lib/
│   │   │   ├── utils.ts
│   │   │   ├── api.ts
│   │   │   └── types.ts
│   │   └── config/
│   │       └── site.ts
│   ├── public/
│   ├── doc/
│   │   ├── frontend-vision.md       # Новый
│   │   ├── frontend-roadmap.md      # Обновлен
│   │   └── plans/
│   │       ├── s1-mock-api-plan.md
│   │       └── s2-frontend-init-plan.md
│   ├── .env.local.example
│   ├── .env.local
│   ├── .eslintrc.json
│   ├── .gitignore
│   ├── .prettierrc
│   ├── .prettierignore
│   ├── components.json
│   ├── next.config.ts
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── postcss.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── README.md
├── doc/
│   ├── adrs/
│   │   ├── ADR-01.md до ADR-06.md   # Существующие
│   │   └── ADR-07-frontend-stack.md # Новый
│   └── ... (остальные)
├── Makefile                         # Обновлен с frontend-* командами
└── README.md                        # Обновлен с frontend секцией
```

## Примечания

- **ADR-07** в общей папке `doc/adrs/` для единой нумерации
- **Только корневой Makefile** с префиксом `frontend-*` для единообразия с `api-*`, `db-*`
- **Темная/светлая тема** настроена с next-themes (работает сразу)
- **Header с навигацией** добавлен для лучшего UX
- **Директория styles/** НЕ создается (не нужна с Tailwind)
- **shadcn/ui charts** упомянут в ADR как предварительный выбор (детали в S3)
- **TypeScript strict mode** аналогично backend (mypy strict)
- **ESLint + Prettier** обеспечивают качество кода аналогично backend (ruff + mypy)

## Зависимости от других спринтов

- **S1 (Mock API)**: ✅ Завершен - backend API готов
- **S3 (Dashboard)**: ⏳ Требует завершения S2
- **S4 (Chat)**: ⏳ Требует завершения S2
- **S5 (Real API)**: ⏳ Не блокирует S2

## Следующие шаги (Sprint S3)

После завершения S2 можно начать Sprint S3 - реализацию дашборда:

1. Установить shadcn/ui charts компоненты
2. Создать компоненты статистических карточек
3. Реализовать графики messages_over_time
4. Интегрировать с Mock API через `getStatistics()`
5. Добавить фильтрацию по периодам (day/week/month/all)
6. Сделать responsive дизайн

### To-dos

- [ ] Создать документ frontend-vision.md с описанием технологий, принципов и архитектуры
- [ ] Инициализировать Next.js проект с TypeScript, Tailwind CSS и App Router
- [ ] Установить и настроить shadcn/ui, добавить базовые компоненты
- [ ] Создать структуру папок (components, lib, config) и базовые файлы
- [ ] Настроить environment variables (.env.local.example, .env.local)
- [ ] Создать TypeScript типы (types.ts) и API клиент (api.ts) для backend интеграции
- [ ] Создать конфигурацию сайта (site.ts) с метаданными
- [ ] Создать root layout с метаданными и глобальными стилями
- [ ] Создать placeholder страницы (home, dashboard, chat)
- [ ] Настроить ESLint, Prettier, TypeScript config и package.json scripts
- [ ] Настроить Next.js конфигурацию (API proxy, rewrites)
- [ ] Создать Makefile команды для frontend разработки
- [ ] Создать README.md для frontend с инструкциями
- [ ] Обновить frontend-roadmap.md и корневой README.md
- [ ] Проверить работоспособность: dev server, type-check, lint, format