# Техническое видение Frontend проекта

## 1. Технологии

### Основной стек

- **Next.js 15+** - современный React framework с App Router
- **TypeScript 5+** - строгая типизация для надежности кода
- **shadcn/ui** - компонентная библиотека высокого качества на базе Radix UI
- **Tailwind CSS** - utility-first CSS framework для быстрой разработки
- **pnpm** - быстрый и эффективный пакетный менеджер
- **lucide-react** - современная библиотека иконок
- **next-themes** - управление темами (dark/light/system)

### Управление зависимостями

- **pnpm** - современный пакетный менеджер с symlinks
- **package.json** - описание проекта и зависимостей
- **pnpm-lock.yaml** - фиксация версий зависимостей

### Инструменты качества кода

- **ESLint** - линтинг кода (next/core-web-vitals, next/typescript)
- **Prettier** - автоматическое форматирование кода
- **TypeScript strict mode** - строгая проверка типов (аналогично backend mypy strict)
- Запуск через npm scripts: `lint`, `format`, `type-check`

---

## 2. Принципы разработки

### Ключевые принципы

- **TypeScript-first** - все компоненты с полной типизацией
- **Component-based** - переиспользуемые компоненты с единой ответственностью
- **DRY (Don't Repeat Yourself)** - избегаем дублирования кода
- **KISS (Keep It Simple, Stupid)** - простота без оверинженеринга
- **Composition over inheritance** - композиция компонентов вместо наследования

### Что используем

- ✅ **Server Components** - использование React Server Components по умолчанию
- ✅ **Client Components** - только где необходима интерактивность ('use client')
- ✅ **TypeScript interfaces** - для всех данных и props
- ✅ **shadcn/ui компоненты** - копируемые компоненты с полным контролем
- ✅ **Tailwind utility classes** - для стилизации компонентов
- ✅ **Custom hooks** - для переиспользования логики

### Что НЕ используем (для простоты)

- ❌ Сложные state management библиотеки (Redux, Zustand) - используем React hooks
- ❌ CSS-in-JS библиотеки - используем Tailwind CSS
- ❌ Тяжелые UI фреймворки (Material-UI, Ant Design) - используем shadcn/ui
- ❌ Избыточная абстракция и сложные паттерны

### Организация компонентов

- **ui/** - базовые shadcn/ui компоненты (Button, Card, Input, etc.)
- **shared/** - переиспользуемые компоненты (Header, ThemeToggle, etc.)
- **dashboard/** - компоненты специфичные для дашборда
- **chat/** - компоненты специфичные для чата
- **lib/** - утилиты, API клиент, типы данных
- **config/** - конфигурация приложения

---

## 3. Архитектура приложения

### Next.js App Router

Используем современный App Router (не Pages Router):

- **File-based routing** - структура файлов определяет роуты
- **Server Components by default** - оптимизация производительности
- **Layouts** - переиспользуемые обертки для страниц
- **Route Groups** - организация роутов без влияния на URL

### Структура роутинга

```
app/
├── layout.tsx          # Root layout (Header, ThemeProvider)
├── page.tsx            # Home page (/)
├── dashboard/
│   └── page.tsx        # Dashboard page (/dashboard)
└── chat/
    └── page.tsx        # Chat page (/chat)
```

### Layouts и композиция

**Root Layout** (`app/layout.tsx`):
- Общий для всех страниц
- Включает: HTML структуру, метаданные, шрифты, ThemeProvider, Header
- Не перерендеривается при навигации

**Page компоненты**:
- Уникальный контент для каждого роута
- Могут быть Server или Client Components
- Композиция из переиспользуемых компонентов

---

## 4. Подход к стилизации

### Tailwind CSS

**Utility-first подход**:
- Классы применяются прямо в JSX
- Быстрая разработка без переключения между файлами
- Консистентный дизайн через design tokens

**Конфигурация** (`tailwind.config.ts`):
- Кастомные цвета для темной/светлой темы
- CSS variables для динамического переключения
- Расширение стандартных утилит при необходимости

### shadcn/ui компоненты

**Копируемые компоненты**:
- Не npm пакет - код копируется в проект
- Полный контроль над компонентами
- Можно модифицировать под свои нужды
- Базируются на Radix UI primitives

**Преимущества**:
- Высокое качество и accessibility
- Консистентный дизайн
- TypeScript типизация из коробки
- Поддержка тем через CSS variables

### Темная/светлая тема

**Реализация через next-themes**:
- Автоматическое переключение dark/light/system
- Сохранение выбора пользователя в localStorage
- Без FOUC (Flash of Unstyled Content)
- CSS variables для динамических цветов

---

## 5. Интеграция с Backend API

### API клиент

**Файл** `lib/api.ts`:
- Функции для всех API endpoints
- Использование нативного `fetch` (Next.js)
- TypeScript типизация запросов и ответов
- Error handling с понятными сообщениями

**Пример**:
```typescript
export async function getStatistics(
  period: 'day' | 'week' | 'month' | 'all' = 'month'
): Promise<Statistics> {
  const response = await fetch(
    `${API_URL}/api/v1/statistics?period=${period}`,
    { cache: 'no-store' }
  );
  
  if (!response.ok) {
    throw new Error(`Failed to fetch: ${response.statusText}`);
  }
  
  return response.json();
}
```

### TypeScript типы

**Файл** `lib/types.ts`:
- Интерфейсы соответствуют backend Pydantic схемам
- Полная типизация данных от API
- Type safety на всех уровнях приложения

### Environment variables

**Конфигурация** (`.env.local`):
- `NEXT_PUBLIC_API_URL` - URL backend API
- Префикс `NEXT_PUBLIC_` для доступа в браузере
- `.env.local.example` в git для примера

### Caching strategy

- **Real-time data** - `cache: 'no-store'` для статистики
- **Static data** - default Next.js caching для статичного контента
- Возможность revalidation в будущем

---

## 6. Инструменты разработки

### ESLint

**Конфигурация** (`.eslintrc.json`):
- `next/core-web-vitals` - best practices Next.js
- `next/typescript` - правила для TypeScript
- Кастомные правила для проекта

### Prettier

**Конфигурация** (`.prettierrc`):
- `singleQuote: true` - одинарные кавычки
- `semi: true` - точки с запятой
- `tabWidth: 2` - 2 пробела для отступов
- Автоформатирование при сохранении (VSCode)

### TypeScript

**Конфигурация** (`tsconfig.json`):
- Strict mode - максимальная проверка типов
- Path aliases - `@/*` для импортов
- Проверка типов: `tsc --noEmit`

### npm scripts

```json
{
  "dev": "next dev",                    // Dev server
  "build": "next build",                // Production build
  "start": "next start",                // Production server
  "lint": "next lint",                  // ESLint проверка
  "lint:fix": "next lint --fix",        // ESLint автофикс
  "format": "prettier --write ...",     // Форматирование
  "format:check": "prettier --check ...", // Проверка форматирования
  "type-check": "tsc --noEmit"          // TypeScript проверка
}
```

---

## 7. Стратегия тестирования

### На будущее (Sprint S3+)

**Unit тесты**:
- Jest + React Testing Library
- Тестирование компонентов изолированно
- Моки для API вызовов

**Integration тесты**:
- Тестирование взаимодействия компонентов
- Проверка API интеграции

**E2E тесты** (опционально):
- Playwright для критичных пользовательских сценариев
- Тестирование полных флоу (навигация, формы, etc.)

### Текущий этап (S2)

- TypeScript компиляция - проверка типов
- ESLint - проверка качества кода
- Prettier - проверка форматирования
- Ручное тестирование в браузере

---

## 8. Сценарии работы пользователя

### Основные use cases

**1. Просмотр дашборда статистики** (Sprint S3):
- Пользователь открывает `/dashboard`
- Загружается статистика за текущий период (month)
- Отображаются карточки с метриками
- Графики показывают динамику сообщений
- Можно переключить период (day/week/month/all)
- Данные обновляются при смене периода

**2. Использование админ-чата** (Sprint S4):
- Пользователь открывает `/chat`
- Видит интерфейс чата
- Может задать вопрос по статистике
- LLM обрабатывает запрос и возвращает ответ
- История диалога сохраняется

**3. Навигация между страницами**:
- Header с ссылками доступен на всех страницах
- Клик на "Dashboard" → переход на `/dashboard`
- Клик на "Chat" → переход на `/chat`
- Клик на логотип → возврат на home `/`

**4. Переключение темы**:
- Кнопка переключателя темы в header
- Клик переключает light ↔ dark
- Выбор сохраняется в localStorage
- Применяется автоматически при следующем визите

**5. Адаптивный дизайн** (S3+):
- Desktop (≥1024px) - полная версия с сайдбаром
- Tablet (768-1023px) - адаптированная версия
- Mobile (<768px) - мобильная версия с бургер-меню

---

## 9. Структура проекта

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   ├── dashboard/          # Dashboard routes
│   │   │   └── page.tsx
│   │   ├── chat/               # Chat routes
│   │   │   └── page.tsx
│   │   └── globals.css         # Global styles
│   ├── components/
│   │   ├── ui/                 # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   └── ...
│   │   ├── shared/             # Shared components
│   │   │   ├── header.tsx
│   │   │   └── theme-toggle.tsx
│   │   ├── dashboard/          # Dashboard components (S3)
│   │   ├── chat/               # Chat components (S4)
│   │   └── theme-provider.tsx  # Theme provider wrapper
│   ├── lib/
│   │   ├── utils.ts            # Utility functions (cn, etc.)
│   │   ├── api.ts              # API client
│   │   └── types.ts            # TypeScript types
│   └── config/
│       └── site.ts             # Site configuration
├── public/                     # Static files
├── doc/                        # Documentation
│   ├── frontend-vision.md      # This file
│   ├── frontend-roadmap.md     # Sprint roadmap
│   └── plans/                  # Sprint plans
├── .env.local.example          # Example env vars
├── .env.local                  # Local env vars (gitignored)
├── .eslintrc.json              # ESLint config
├── .gitignore                  # Git ignore patterns
├── .prettierrc                 # Prettier config
├── .prettierignore             # Prettier ignore patterns
├── components.json             # shadcn/ui config
├── next.config.ts              # Next.js config
├── package.json                # Dependencies & scripts
├── pnpm-lock.yaml              # Lock file
├── postcss.config.js           # PostCSS config
├── tailwind.config.ts          # Tailwind config
├── tsconfig.json               # TypeScript config
└── README.md                   # Frontend README
```

---

## 10. Предварительный выбор библиотек

### Для дашборда (Sprint S3)

**Charts библиотека**: shadcn/ui charts (предварительно)
- Обертка над Recharts с shadcn/ui стилями
- Единообразие с остальными компонентами
- TypeScript типизация
- Поддержка тем из коробки
- Альтернативы: Recharts, Chart.js, Tremor

**Преимущества shadcn/ui charts**:
- Консистентный дизайн с остальным UI
- Копируемые компоненты (можно кастомизировать)
- Автоматическая поддержка dark/light темы
- Хорошая документация и примеры

---

## 11. Deployment (будущее)

### Текущий этап (S2-S4)

- Локальная разработка: `pnpm dev`
- Production build: `pnpm build`
- Production server: `pnpm start`

### Возможные варианты деплоя (после S4)

**Vercel** (рекомендуется):
- Нативная поддержка Next.js
- Автоматический деплой из git
- Edge functions и optimizations
- Бесплатный tier для малых проектов

**Альтернативы**:
- Docker + VPS (полный контроль)
- Netlify (хорошая альтернатива Vercel)
- AWS Amplify (если используется AWS инфраструктура)

---

## 12. Интеграция с Backend

### Окружения

**Development**:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Next.js rewrites: `/api/*` → `http://localhost:8000/api/*`

**Production** (будущее):
- Frontend: `https://yourdomain.com`
- Backend API: `https://api.yourdomain.com`
- CORS настройка на backend
- Environment variables через hosting platform

### API Endpoints

**Используемые в проекте**:
- `GET /api/v1/statistics?period={day|week|month|all}` - статистика (S3)
- Future endpoints для чата (S4)

---

## 13. Best Practices

### Code Style

- **Именование компонентов**: PascalCase (Button, ThemeToggle)
- **Именование файлов**: kebab-case для утилит, PascalCase для компонентов
- **Именование функций**: camelCase (getStatistics, handleClick)
- **Константы**: UPPER_SNAKE_CASE (API_URL)

### Component Guidelines

- **Single Responsibility** - один компонент = одна задача
- **Props типизация** - всегда TypeScript interfaces
- **Composition** - переиспользование через композицию
- **Client boundary** - минимизация 'use client' директив

### Performance

- **Server Components по умолчанию** - меньше JavaScript в браузере
- **Image optimization** - использование next/image
- **Font optimization** - использование next/font
- **Code splitting** - автоматически через App Router

---

## 14. Соответствие Backend подходу

### Аналогии с Backend

| Backend | Frontend |
|---------|----------|
| `mypy strict` | TypeScript strict mode |
| `ruff format` | Prettier |
| `ruff check` | ESLint |
| `pytest` | (будущие тесты) |
| `Makefile` | Makefile с `frontend-*` командами |
| `uv` | pnpm |
| Python type hints | TypeScript interfaces |
| Pydantic models | TypeScript types |

### Общие принципы

- ✅ Строгая типизация везде
- ✅ Автоматические проверки качества
- ✅ Минимум внешних зависимостей
- ✅ Документированный код
- ✅ KISS принцип
- ✅ DRY принцип

---

## 15. Что НЕ входит в текущий scope

### Не реализуется в S2

- ❌ Реальные данные дашборда (Sprint S3)
- ❌ Функционал чата (Sprint S4)
- ❌ Аутентификация/авторизация
- ❌ Сложный state management
- ❌ E2E тесты
- ❌ Production deployment
- ❌ CI/CD pipeline
- ❌ Мониторинг и аналитика

### Приоритеты S2

✅ Инициализация проекта
✅ Базовая структура и конфигурация
✅ Инструменты разработки
✅ Placeholder страницы
✅ Навигация и темы
✅ API клиент и типы
✅ Документация

---

## 16. Следующие шаги

### После завершения S2

**Sprint S3** - Реализация дашборда:
1. Установка shadcn/ui charts
2. Создание компонентов статистики
3. Интеграция с Mock API
4. Фильтрация по периодам
5. Responsive дизайн

**Sprint S4** - Реализация чата:
1. UI чата
2. Backend API для чата
3. Интеграция с LLM
4. История сообщений

**Sprint S5** - Переход на Real API:
1. Замена Mock на Real StatCollector
2. Интеграция с PostgreSQL
3. Тестирование с реальными данными

---

