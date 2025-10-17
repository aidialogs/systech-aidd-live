# План Спринта F2: Каркас frontend проекта

## Обзор

Создание структуры frontend проекта с использованием выбранного технологического стека: Next.js, React, TypeScript, shadcn/ui, Tailwind CSS, pnpm. Документирование архитектурных решений и настройка инструментов разработки.

## Ключевые файлы

- `frontend/doc/frontend-vision.md` - техническое видение frontend части
- `doc/adrs/ADR-07.md` - ADR с обоснованием выбора технологического стека
- `frontend/package.json` - зависимости и скрипты проекта
- `frontend/app/` - структура Next.js приложения (App Router)
- `Makefile` - команды для работы с frontend

## Шаги реализации

### 1. Создание документа frontend-vision.md

Создать `frontend/doc/frontend-vision.md` по аналогии с `doc/vision.md`, включающий:

**Структура документа:**

- Раздел 1: Технологии
  - Основной стек: Next.js 15+, React 18+, TypeScript 5+, shadcn/ui, Tailwind CSS
  - Пакетный менеджер: pnpm
  - Инструменты качества кода: ESLint, Prettier, TypeScript strict mode

- Раздел 2: Принципы разработки
  - KISS принцип - минимум оверинжиниринга
  - Компонентный подход - переиспользуемые UI компоненты
  - Type safety - строгая типизация TypeScript
  - Server Components first - использование RSC где возможно

- Раздел 3: Структура проекта
  ```
  frontend/
  ├── app/                    # Next.js App Router
  │   ├── layout.tsx         # Корневой layout
  │   ├── page.tsx           # Главная страница
  │   └── api/               # API routes (проксирование к backend)
  ├── components/
  │   ├── ui/                # shadcn/ui компоненты
  │   └── ...                # Кастомные компоненты
  ├── lib/                   # Утилиты и helpers
  ├── types/                 # TypeScript типы
  ├── public/                # Статические файлы
  ├── package.json
  ├── tsconfig.json
  └── tailwind.config.ts
  ```

- Раздел 4: Архитектура приложения
  - Dashboard: отображение статистики через API
  - Admin Chat: веб-интерфейс для администраторов
  - API Integration: работа с backend через fetch/axios

- Раздел 5: Интеграция с Backend
  - API endpoints из Sprint F1: `GET /api/stats?period={7d|30d}`
  - Mock API для разработки frontend
  - Переход на real API в Sprint F5

- Раздел 6: Локальный запуск
  - Команды: `make frontend-install`, `make frontend-dev`
  - Dev server на `http://localhost:3000`
  - Backend API на `http://localhost:8000`

### 2. Создание ADR-07 для фиксации технологического стека

Создать `doc/adrs/ADR-07.md` с обоснованием выбора:

**Структура ADR:**

- Статус: Принято
- Дата: 2025-10-17
- Контекст: необходимость выбора технологий для frontend
- Решение: Next.js + React + TypeScript + shadcn/ui + Tailwind CSS + pnpm

**Обоснование выбора:**

**Next.js 15:**

- ✅ App Router - современная маршрутизация
- ✅ Server Components - оптимизация производительности
- ✅ API Routes - проксирование запросов к backend
- ✅ Built-in оптимизации (Image, Font, Script)
- ✅ TypeScript поддержка из коробки

**TypeScript:**

- ✅ Статическая типизация - меньше ошибок
- ✅ Лучший DX с автодополнением
- ✅ Strict mode для максимальной безопасности
- ✅ Интеграция с shadcn/ui

**shadcn/ui:**

- ✅ Копирование компонентов в проект (не npm пакет)
- ✅ Полный контроль над кодом компонентов
- ✅ Radix UI primitives - accessibility из коробки
- ✅ Tailwind CSS стилизация
- ✅ Готовые dashboard блоки

**Tailwind CSS:**

- ✅ Utility-first подход - быстрая разработка
- ✅ Встроенная поддержка темной темы
- ✅ Адаптивный дизайн через breakpoints
- ✅ Оптимизация через PurgeCSS

**pnpm:**

- ✅ Быстрая установка зависимостей
- ✅ Эффективное использование дискового пространства
- ✅ Строгая изоляция зависимостей
- ✅ Monorepo support (если понадобится)

**Альтернативы:**

- Vite + React: отклонено (меньше возможностей SSR)
- Create React App: deprecated
- Vue/Svelte: отклонено (команда знает React)
- Material UI / Ant Design: отклонено (слишком тяжелые)

### 3. Инициализация Next.js проекта

Создать Next.js проект в директории `frontend/`:

```bash
cd /Users/akozhin/projects/systech-aidd-live
pnpm create next-app@latest frontend \
  --typescript \
  --tailwind \
  --app \
  --src-dir=false \
  --import-alias="@/*" \
  --no-git
```

Параметры:

- `--typescript` - использовать TypeScript
- `--tailwind` - установить Tailwind CSS
- `--app` - использовать App Router (не Pages Router)
- `--src-dir=false` - без src/ директории (app/ в корне)
- `--import-alias="@/*"` - алиасы для импортов
- `--no-git` - не инициализировать новый git репозиторий

### 4. Установка и настройка shadcn/ui

Инициализировать shadcn/ui в проекте:

```bash
cd frontend
pnpm dlx shadcn@latest init -d
```

Параметр `-d` - использовать default настройки:

- Style: Default
- Base color: Slate
- CSS variables: Yes

Добавить первые компоненты для проверки:

```bash
pnpm dlx shadcn@latest add button card
```

### 5. Настройка TypeScript strict mode

Обновить `frontend/tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true
  }
}
```

### 6. Настройка ESLint и Prettier

Создать `frontend/.eslintrc.json`:

```json
{
  "extends": ["next/core-web-vitals", "next/typescript"],
  "rules": {
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/no-explicit-any": "warn"
  }
}
```

Создать `frontend/.prettierrc`:

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": false,
  "tabWidth": 2,
  "printWidth": 100
}
```

Добавить `.prettierignore`:

```
.next
node_modules
pnpm-lock.yaml
```

### 7. Создание базовой структуры компонентов

Создать структуру директорий:

```
frontend/
├── components/
│   ├── ui/           # shadcn/ui компоненты (генерируются автоматически)
│   ├── dashboard/    # Компоненты дашборда
│   └── chat/         # Компоненты чата
├── lib/
│   └── utils.ts      # Утилиты (создается shadcn/ui)
├── types/
│   └── api.ts        # TypeScript типы для API
└── app/
    ├── layout.tsx
    ├── page.tsx
    └── globals.css
```

### 8. Обновление Makefile

Добавить команды для frontend в корневой `Makefile`:

```makefile
# Frontend commands
frontend-install:
	cd frontend && pnpm install

frontend-dev:
	cd frontend && pnpm dev

frontend-build:
	cd frontend && pnpm build

frontend-start:
	cd frontend && pnpm start

frontend-lint:
	cd frontend && pnpm lint

frontend-format:
	cd frontend && pnpm format

frontend-type-check:
	cd frontend && pnpm tsc --noEmit

frontend-check-all: frontend-lint frontend-type-check
```

### 9. Обновление package.json скриптов

Добавить скрипты в `frontend/package.json`:

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  }
}
```

### 10. Создание .gitignore для frontend

Добавить в `frontend/.gitignore`:

```
# dependencies
/node_modules
/.pnp
.pnp.js

# next.js
/.next/
/out/

# production
/build

# misc
.DS_Store
*.pem

# debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# local env files
.env*.local

# vercel
.vercel

# typescript
*.tsbuildinfo
next-env.d.ts
```

### 11. Обновление frontend/README.md

Создать документацию по запуску:

```markdown
# Frontend - systech-aidd-live

## Технологический стек

- Framework: Next.js 15+
- Язык: TypeScript 5+
- UI Library: shadcn/ui
- Styling: Tailwind CSS
- Пакетный менеджер: pnpm

## Быстрый старт

### Установка зависимостей
\`\`\`bash
make frontend-install
\`\`\`

### Запуск dev-сервера
\`\`\`bash
make frontend-dev
\`\`\`

Приложение будет доступно на http://localhost:3000

### Проверка качества кода
\`\`\`bash
make frontend-check-all
\`\`\`

## Команды разработки

- `make frontend-dev` - запуск dev-сервера
- `make frontend-build` - production сборка
- `make frontend-lint` - проверка ESLint
- `make frontend-format` - форматирование кода
- `make frontend-type-check` - проверка типов TypeScript

## Структура проекта

См. `doc/frontend-vision.md`
```

### 12. Обновление frontend-roadmap.md

Обновить статус Sprint F2 и добавить ссылку на план:

```markdown
| **F2** | Каркас frontend проекта | ✅ Завершен | [План F2](.cursor/plans/...) |
```

## Критерии готовности

- ✅ Создан документ `frontend/doc/frontend-vision.md`
- ✅ Создан ADR-07 в `doc/adrs/ADR-07.md`
- ✅ Инициализирован Next.js проект в `frontend/`
- ✅ Установлен и настроен shadcn/ui
- ✅ Настроены ESLint, Prettier, TypeScript strict mode
- ✅ Добавлены команды в Makefile для работы с frontend
- ✅ Dev-сервер запускается на `http://localhost:3000`
- ✅ `make frontend-check-all` проходит без ошибок
- ✅ Обновлена документация в README.md

## Примечания

- Проект создается внутри директории `frontend/`
- ADR размещается в общей директории `doc/adrs/` (с backend ADR)
- Frontend vision следует структуре backend `doc/vision.md`
- Все команды выполняются через Makefile для консистентности
- pnpm используется как единый пакетный менеджер для frontend

## Статус выполнения

**Дата начала:** 2025-10-17  
**Дата завершения:** 2025-10-17  
**Статус:** ✅ Завершен

### Выполненные задачи

- ✅ Создан `frontend/doc/frontend-vision.md` с описанием архитектуры и принципов разработки
- ✅ Создан `doc/adrs/ADR-07.md` с обоснованием выбора технологического стека
- ✅ Инициализирован Next.js проект в директории `frontend/` с TypeScript и Tailwind CSS
- ✅ Установлен и настроен shadcn/ui, добавлены компоненты button и card
- ✅ Настроен TypeScript strict mode, ESLint, Prettier
- ✅ Создана базовая структура директорий (components/, lib/, types/)
- ✅ Добавлены команды для frontend в корневой Makefile
- ✅ Обновлен `frontend/README.md` и `frontend/doc/frontend-roadmap.md`

### Результаты

**Технологический стек:**
- Next.js 15.5.6
- React 19.1.0
- TypeScript 5.9.3
- shadcn/ui (Radix UI + Tailwind)
- Tailwind CSS 4.1.14
- pnpm 10.16.1

**Команды разработки:**
```bash
make frontend-install      # Установка зависимостей
make frontend-dev          # Запуск dev-сервера (порт 3000)
make frontend-check-all    # Проверка качества кода (lint + types)
```

**Доступные документы:**
- `frontend/doc/frontend-vision.md` - техническое видение
- `doc/adrs/ADR-07.md` - ADR выбора технологий
- `frontend/README.md` - руководство по работе с проектом

