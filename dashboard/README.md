# Dashboard Frontend

Статистика Telegram бота с визуализацией метрик.

> Техническое видение: [doc/front-vision.md](doc/front-vision.md)  
> ADR стека: [../doc/adrs/ADR-06.md](../doc/adrs/ADR-06.md)  
> Правила разработки: [../.cursor/rules/conventions-front.mdc](../.cursor/rules/conventions-front.mdc)

---

## Технологии

- **Next.js 14** (App Router)
- **shadcn/ui** + Tailwind CSS
- **TypeScript** strict mode
- **pnpm** package manager

## Установка

```bash
pnpm install
```

## Конфигурация

```bash
cp .env.example .env.local
```

Настроить `NEXT_PUBLIC_API_URL` в `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Запуск

```bash
pnpm dev          # dev сервер → http://localhost:3000
pnpm build        # production сборка
pnpm start        # production сервер
pnpm lint         # ESLint проверка
pnpm type-check   # TypeScript проверка типов
```

## Структура проекта

```
dashboard/
├── doc/              # Документация
├── app/              # Next.js pages (App Router)
├── components/       # React компоненты
│   ├── ui/          # shadcn/ui компоненты
│   └── *.tsx        # кастомные компоненты
├── lib/             # Утилиты и API клиент
├── types/           # TypeScript интерфейсы
└── public/          # Статические файлы
```

## Разработка

### Добавление shadcn/ui компонента

```bash
pnpm dlx shadcn@latest add <component-name>
```

### Проверка качества кода

```bash
pnpm type-check   # TypeScript типы
pnpm lint         # ESLint
pnpm build        # Production сборка
```

### Правила разработки

- **TypeScript strict mode** - обязательно
- **Один компонент = один файл**
- **Tailwind CSS** для стилизации
- **Все props типизированы**
- **Loading и error states обязательны**

См. полные правила в [conventions-front.mdc](../.cursor/rules/conventions-front.mdc)

## Backend Integration

Frontend подключается к FastAPI backend через REST API:

```
GET /api/stats
```

Response: JSON с метриками (см. `types/stats.ts`)

## MVP Features

- ✅ Overview Cards (4 метрики с трендами)
- ✅ Message Activity Graph (line chart)
- ✅ Темная/светлая тема
- ✅ Responsive design

## Ограничения MVP

- ❌ Без авторизации
- ❌ Только чтение данных
- ❌ Polling вместо WebSocket
- ❌ Локальный запуск

---

**Готов к расширению:** Top Users Table, Recent Conversations Table, фильтры, и другие компоненты.
