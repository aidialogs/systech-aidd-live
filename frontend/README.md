# Frontend - systech-aidd-live

Пользовательский интерфейс для проекта systech-aidd-live, включающий дашборд статистики и веб-чат для администрирования.

## Технологический стек

- **Framework:** Next.js 15+
- **Язык:** TypeScript 5+
- **UI Library:** shadcn/ui
- **Styling:** Tailwind CSS 4+
- **Пакетный менеджер:** pnpm

## Быстрый старт

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

Приложение будет доступно на **http://localhost:3000**

### Проверка качества кода

```bash
make frontend-check-all
```

Это выполнит ESLint проверку и TypeScript type check.

## Команды разработки

### Просмотр всех команд

```bash
make help
```

Или просто:

```bash
make
```

### Основные команды

- `make frontend-install` - установка зависимостей (pnpm)
- `make frontend-dev` - запуск dev-сервера (порт 3000)
- `make frontend-build` - production сборка
- `make frontend-start` - запуск production сервера

### Проверка качества

- `make frontend-lint` - проверка ESLint
- `make frontend-format` - форматирование кода через Prettier
- `make frontend-type-check` - проверка TypeScript типов
- `make frontend-check-all` - полная проверка (lint + types)

> **Примечание:** Все frontend команды автоматически используют правильную версию Node.js через nvm.

### Прямые команды (через pnpm)

```bash
cd frontend

pnpm dev          # Запуск dev-сервера
pnpm build        # Production сборка
pnpm start        # Запуск production сервера
pnpm lint         # ESLint проверка
pnpm format       # Prettier форматирование
pnpm type-check   # TypeScript проверка
```

## Структура проекта

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Корневой layout
│   ├── page.tsx           # Главная страница (dashboard)
│   └── globals.css        # Глобальные стили
├── components/
│   ├── ui/                # shadcn/ui компоненты (button, card, etc.)
│   ├── dashboard/         # Компоненты дашборда (будущее)
│   └── chat/              # Компоненты чата (будущее)
├── lib/
│   ├── utils.ts           # Утилиты (cn helper)
│   └── api.ts             # API client для backend
├── types/
│   └── api.ts             # TypeScript типы для API
├── doc/                   # Документация
│   ├── frontend-vision.md
│   ├── frontend-roadmap.md
│   ├── dashboard-requirements.md
│   └── sprint-f1-summary.md
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── components.json        # Конфигурация shadcn/ui
└── eslint.config.mjs
```

## Интеграция с Backend

Frontend взаимодействует с FastAPI backend через REST API.

### API Endpoints

- `GET /api/stats?period={7d|30d}` - получение статистики
- `GET /health` - проверка здоровья API

### Переменные окружения

Создайте файл `.env.local` в директории `frontend/`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Запуск backend API

В отдельном терминале:

```bash
make api-run
```

Backend API будет доступен на **http://localhost:8000**

Документация API: **http://localhost:8000/docs**

## Разработка

### Добавление shadcn/ui компонентов

```bash
cd frontend
pnpm dlx shadcn@latest add [component-name]
```

Например:

```bash
pnpm dlx shadcn@latest add button
pnpm dlx shadcn@latest add card
pnpm dlx shadcn@latest add input
```

### Форматирование кода

```bash
make frontend-format
```

Это отформатирует все файлы согласно настройкам Prettier.

### Проверка перед коммитом

```bash
make frontend-check-all
```

Убедитесь, что все проверки проходят перед коммитом изменений.

## Roadmap

См. [frontend-roadmap.md](doc/frontend-roadmap.md) для детального плана развития.

### Спринты

- **F1:** ✅ Требования к дашборду и Mock API
- **F2:** ✅ Каркас frontend проекта (текущий)
- **F3:** 📋 Реализация dashboard
- **F4:** 📋 Реализация ИИ-чата
- **F5:** 📋 Переход на реальный API

## Документация

- [Техническое видение](doc/frontend-vision.md) - архитектура и принципы разработки
- [Roadmap](doc/frontend-roadmap.md) - план развития frontend
- [Dashboard Requirements](doc/dashboard-requirements.md) - требования к дашборду
- [ADR-07](../doc/adrs/ADR-07.md) - решение о выборе технологического стека

## Ресурсы

- [Next.js Documentation](https://nextjs.org/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
