# Техническое видение Frontend проекта

## 1. Технологии

### Основной стек

- **Next.js 15** - React framework с Server-Side Rendering
- **React 19** - библиотека для построения UI
- **TypeScript 5.x** - статическая типизация JavaScript
- **pnpm 9.x** - быстрый и эффективный менеджер пакетов

### UI компоненты и стилизация

- **shadcn/ui** - коллекция копируемых компонентов (copy-paste в проект)
- **Radix UI** - примитивы для доступных компонентов (под капотом shadcn/ui)
- **Tailwind CSS 4.x** - utility-first CSS framework
- **Lucide React** - иконки (поставляются с shadcn/ui)

### Charts и визуализация

- **Recharts** - declarative charts для React
- Альтернативы (если потребуется): visx, Chart.js

### HTTP client

- **Native fetch API** - встроенный в браузер и Next.js
- TypeScript wrappers для типизации requests/responses
- Без axios/ky (KISS принцип)

### State management

- **React hooks** (useState, useReducer) - для локального состояния
- **Server Components** - для server-side data
- **React Context** (при необходимости) - для глобального состояния
- Без Redux/Zustand/MobX (KISS принцип)

### Инструменты качества кода

- **ESLint** - статический анализ кода
- **Prettier** - форматирование кода
- **TypeScript strict mode** - максимальная типизация

### Testing (будущее)

- **Vitest** - быстрый test runner (Vite-powered)
- **React Testing Library** - тестирование компонентов
- **Playwright** - E2E тестирование (опционально)

---

## 2. Принципы разработки

### Ключевые принципы

- **KISS (Keep It Simple, Stupid)** - никакого оверинжиниринга, только необходимое
- **Type Safety First** - строгая типизация всего кода (как в backend)
- **Component-First** - переиспользуемые, композируемые компоненты
- **Accessibility First** - WCAG 2.1 AA compliance из коробки
- **Mobile First** - responsive design с приоритетом на мобильные устройства
- **Server Components First** - использовать React Server Components где возможно

### Что НЕ используем (для простоты)

- ❌ Redux / Zustand / MobX - достаточно React hooks + Server Components
- ❌ GraphQL - REST API достаточно для нашего случая
- ❌ Сложные формы и validation - нет форм в текущем scope
- ❌ i18n - пока только английский язык
- ❌ Authentication - будет добавлено позже если потребуется
- ❌ React Query / SWR - достаточно native fetch + Server Components
- ❌ Styled Components / Emotion - используем Tailwind CSS
- ❌ Storybook - не нужен для простого dashboard

### Что используем для качества кода

- ✅ **Type hints** - обязательны для всех функций и компонентов
- ✅ **Interfaces** - для структур данных (API responses, component props)
- ✅ **ESLint** - с правилами TypeScript и React
- ✅ **Prettier** - единообразное форматирование
- ✅ **TypeScript strict mode** - максимальная проверка типов

### Стиль кода

- Следуем **Airbnb React Style Guide** (базовые принципы)
- Функциональные компоненты (не классы)
- Hooks для state management
- Destructuring для props
- Named exports для компонентов

---

## 3. Структура проекта

### Организация файлов

```
frontend/
├── app/                         # Next.js App Router
│   ├── layout.tsx              # Root layout (metadata, fonts)
│   ├── page.tsx                # Dashboard page
│   ├── globals.css             # Global styles (Tailwind directives)
│   └── error.tsx               # Error boundary (будущее)
├── components/
│   ├── ui/                     # shadcn/ui components (копируются в проект)
│   │   ├── card.tsx
│   │   ├── button.tsx
│   │   └── badge.tsx
│   ├── dashboard/              # Dashboard-specific components
│   │   ├── metric-card.tsx    # Карточка метрики
│   │   └── messages-chart.tsx # График сообщений
│   └── layout/                 # Layout components
│       ├── header.tsx          # Шапка приложения
│       └── nav.tsx             # Навигация (будущее)
├── lib/
│   ├── api.ts                  # API client для backend
│   ├── utils.ts                # Utility functions (cn, formatters)
│   └── types.ts                # TypeScript types/interfaces
├── public/                     # Static assets
│   ├── favicon.ico
│   └── images/
├── doc/                        # Documentation
│   ├── front-vision.md         # Этот документ
│   ├── dashboard-requirements.md
│   └── frontend-roadmap.md
├── .eslintrc.json              # ESLint configuration
├── .prettierrc                 # Prettier configuration
├── .gitignore
├── tailwind.config.ts          # Tailwind configuration
├── tsconfig.json               # TypeScript configuration
├── next.config.ts              # Next.js configuration
├── package.json                # Dependencies and scripts
├── pnpm-lock.yaml              # Lockfile
└── README.md                   # Frontend documentation
```

### Принципы организации

- **Плоская структура компонентов** - components разбиты по назначению (ui, dashboard, layout)
- **Colocation** - держать связанные файлы рядом
- **Один компонент = один файл** - строгое правило
- **Минимум файлов** - только необходимое для работы

---

## 4. Архитектура приложения

### Компонентная архитектура

```
┌─────────────────────────────────────────┐
│  app/layout.tsx (Root Layout)           │
│  - Metadata, Fonts, Global Styles       │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│  app/page.tsx (Dashboard Page)          │
│  - Server Component                     │
│  - Fetches data from API                │
└────────────┬────────────────────────────┘
             ↓
     ┌───────┴───────┐
     ↓               ↓
┌─────────┐   ┌──────────────┐
│ Metric  │   │   Messages   │
│  Cards  │   │    Chart     │
│  (x4)   │   │ (Client Cmp) │
└─────────┘   └──────────────┘
```

### Server Components vs Client Components

**Server Components (по умолчанию):**

- `app/page.tsx` - dashboard page с data fetching
- `app/layout.tsx` - root layout
- Статические компоненты без интерактивности

**Client Components ("use client"):**

- `components/dashboard/messages-chart.tsx` - интерактивный график
- Компоненты с hooks (useState, useEffect)
- Компоненты с event handlers

### Data Fetching стратегия

**Server-side (предпочтительно):**

```typescript
// app/page.tsx
async function DashboardPage() {
  const stats = await fetch('http://localhost:8000/api/stats')
  return <Dashboard data={stats} />
}
```

**Client-side (при необходимости):**

```typescript
// components/dashboard/messages-chart.tsx
"use client";
export function MessagesChart() {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetch("/api/stats").then(setData);
  }, []);
}
```

### Типизация

**Строгие TypeScript interfaces:**

```typescript
// lib/types.ts
export interface MetricCard {
  title: string;
  value: string;
  trend: string;
  description: string;
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

**Type-safe API client:**

```typescript
// lib/api.ts
export async function fetchDashboardStats(): Promise<DashboardStats> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/stats`);
  if (!response.ok) throw new Error("Failed to fetch stats");
  return response.json();
}
```

### Error Handling

- **Error boundaries** - для перехвата React ошибок
- **Try-catch** - для async операций
- **Fallback UI** - для loading и error states
- **User-friendly messages** - понятные сообщения об ошибках

---

## 5. API Integration

### Backend API

- **Base URL**: `http://localhost:8000` (dev), `https://api.example.com` (prod)
- **Endpoint**: `GET /api/stats`
- **Format**: JSON
- **CORS**: настроен в FastAPI backend для `http://localhost:3000`

### API Client

```typescript
// lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchDashboardStats(): Promise<DashboardStats> {
  const response = await fetch(`${API_BASE_URL}/api/stats`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    // Next.js caching strategy
    next: { revalidate: 60 }, // Revalidate every 60 seconds
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}
```

### Environment Variables

```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

- `NEXT_PUBLIC_*` - доступны в браузере
- Без префикса - только на сервере

---

## 6. UX/UI принципы

### Основные принципы

1. **Consistency** - единообразие интерфейса во всем приложении
2. **Instant Feedback** - мгновенная обратная связь на действия пользователя
3. **Error Recovery** - понятные сообщения об ошибках и способы их исправления
4. **Performance** - быстрый отклик интерфейса (< 3s Time to Interactive)
5. **Accessibility** - доступность для всех пользователей (WCAG 2.1 AA)

### Loading States

- **Skeletons** - для метрик и графиков во время загрузки
- **Spinners** - для точечных операций
- **Progress bars** - для длительных операций (если потребуется)

### Error States

- **Error messages** - понятные сообщения на естественном языке
- **Retry buttons** - возможность повторить запрос
- **Fallback UI** - graceful degradation при ошибках

### Responsive Design

- **Mobile First** - приоритет мобильной версии
- **Breakpoints**: sm (640px), md (768px), lg (1024px), xl (1280px)
- **Tailwind classes**: `sm:`, `md:`, `lg:`, `xl:` для адаптивности

### Accessibility

- **Semantic HTML** - правильные теги (header, nav, main, article)
- **ARIA labels** - для screen readers (через Radix UI)
- **Keyboard navigation** - Tab, Enter, Escape, стрелки
- **Focus visible** - видимый focus state для клавиатуры
- **Color contrast** - WCAG AA compliance (4.5:1 для текста)

---

## 7. Styling стратегия

### Tailwind CSS подход

**Utility classes в JSX:**

```tsx
<div className="flex items-center gap-4 rounded-lg bg-white p-6 shadow">
  <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
</div>
```

**Композиция через компоненты:**

```tsx
// Вместо дублирования классов - создаем компонент
function Card({ children, className }) {
  return <div className={cn("rounded-lg bg-white p-6 shadow", className)}>{children}</div>;
}
```

**Утилита cn() для условных классов:**

```typescript
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### shadcn/ui компоненты

- Копируются в `components/ui/`
- Можно модифицировать под нужды проекта
- Стилизованы через Tailwind CSS
- Полный контроль над кодом

### Global Styles

```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom base styles */
@layer base {
  body {
    @apply bg-gray-50 text-gray-900;
  }
}
```

---

## 8. Инструменты качества кода

### ESLint

**Конфигурация:**

```json
{
  "extends": ["next/core-web-vitals", "plugin:@typescript-eslint/recommended", "prettier"],
  "rules": {
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
    "@typescript-eslint/no-explicit-any": "error",
    "prefer-const": "error"
  }
}
```

**Команды:**

- `pnpm lint` - проверка кода
- `pnpm lint --fix` - автоисправление

### Prettier

**Конфигурация:**

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

**Команды:**

- `pnpm format` - форматирование всех файлов

### TypeScript Strict Mode

**tsconfig.json:**

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noImplicitReturns": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

**Команды:**

- `pnpm type-check` - проверка типов без компиляции

### Проверка перед коммитом

```bash
pnpm format  # Форматирование
pnpm lint    # Линтинг
pnpm type-check  # Проверка типов
pnpm build   # Сборка проекта
```

---

## 9. Performance оптимизация

### Next.js оптимизации

- **Code Splitting** - автоматическое разбиение на chunks
- **Image Optimization** - `next/image` компонент для оптимизации изображений
- **Font Optimization** - `next/font` для оптимизации шрифтов
- **Server Components** - уменьшение JavaScript на клиенте

### Caching стратегия

```typescript
// Revalidate every 60 seconds
fetch(url, { next: { revalidate: 60 } });

// No caching (always fresh)
fetch(url, { cache: "no-store" });

// Cache indefinitely (until manual revalidation)
fetch(url, { cache: "force-cache" });
```

### Metrics

- **Lighthouse score** - target > 90
- **Bundle size** - initial load < 200KB (gzipped)
- **Time to Interactive** - < 3 seconds
- **First Contentful Paint** - < 1.5 seconds

---

## 10. Локальный запуск

### Требования

- Node.js 18+ (LTS)
- pnpm 9+
- Backend API запущен на `http://localhost:8000`

### Установка зависимостей

```bash
cd frontend
pnpm install
```

### Запуск dev сервера

```bash
pnpm dev
```

Приложение доступно на `http://localhost:3000`

### Build production

```bash
pnpm build
pnpm start
```

### Команды

```json
{
  "scripts": {
    "dev": "next dev", // Development server
    "build": "next build", // Production build
    "start": "next start", // Start production server
    "lint": "next lint", // Run ESLint
    "format": "prettier --write \"**/*.{ts,tsx,json,md}\"", // Format code
    "type-check": "tsc --noEmit" // Type checking
  }
}
```

---

## 11. Deployment

### Deployment стратегии

**1. Vercel (рекомендуется):**

- Нативная поддержка Next.js
- Автоматический deploy из git
- Edge Network для быстрой доставки
- Free tier для личных проектов

**2. Netlify:**

- Аналогично Vercel
- Простой deploy из git
- Free tier доступен

**3. Self-hosted (Docker):**

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile
COPY . .
RUN pnpm build
EXPOSE 3000
CMD ["pnpm", "start"]
```

### Environment Variables

**Production:**

```env
NEXT_PUBLIC_API_URL=https://api.example.com
NODE_ENV=production
```

---

## 12. Roadmap и будущие улучшения

### Короткий срок (Sprint S3)

- ✅ Реализация dashboard компонентов
- ✅ Интеграция с MockAPI
- ✅ Responsive layout
- ✅ Error handling

### Средний срок (Sprint S4)

- Real-time обновления (WebSocket или polling)
- Дополнительные метрики
- Фильтрация по датам

### Долгий срок (Sprint S5+)

- Authentication/Authorization
- User management
- Export данных (CSV, Excel)
- Advanced analytics

---

## 13. Связь с Backend

### Соответствие принципам

| Backend (Python)     | Frontend (TypeScript)    |
| -------------------- | ------------------------ |
| Type hints           | TypeScript types         |
| Dataclasses          | Interfaces               |
| KISS principle       | KISS principle           |
| One class = one file | One component = one file |
| Repository pattern   | API client abstraction   |
| Async/await          | Async/await              |
| Strict typing (mypy) | Strict mode (TypeScript) |

### API Contract

Типы frontend генерируются на основе backend API schema:

- Backend: `DashboardStats` (Python dataclass)
- Frontend: `DashboardStats` (TypeScript interface)

---

**Версия документа**: 1.0  
**Дата создания**: 2025-10-16  
**Статус**: Активное техническое видение
