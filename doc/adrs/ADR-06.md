# ADR-06: Выбор технологического стека Frontend Dashboard

**Статус:** Принято  
**Дата:** 2025-10-15  
**Авторы:** Команда разработки

## Контекст

Для визуализации статистики Telegram бота необходимо создать web dashboard с современным UI. Требования:

- Отображение метрик в реальном времени (Overview Cards, Message Activity Graph)
- Темная/светлая тема
- Responsive design
- Быстрая разработка MVP
- Готовность к расширению (добавление таблиц, новых метрик)
- Интеграция с FastAPI backend через REST API

## Решение

Выбран стек **Next.js 14 + shadcn/ui + pnpm + TypeScript strict + Tailwind CSS** для разработки frontend dashboard.

### Компоненты решения:

1. **Framework**: Next.js 14 (App Router)
2. **UI Components**: shadcn/ui
3. **Package Manager**: pnpm
4. **Language**: TypeScript strict mode
5. **Styling**: Tailwind CSS
6. **Charts**: shadcn/ui charts (recharts wrapper)

## Обоснование выбора

### Next.js 14

**Преимущества:**
- Server Components и App Router из коробки - современная архитектура React
- Производительность: автоматический code splitting, image optimization, route prefetching
- SSR/SSG для быстрой первой загрузки (<2 сек)
- Встроенный TypeScript support без дополнительной настройки
- API Routes (не нужны сейчас, но полезны для будущего прокси к backend)
- Огромное сообщество и отличная документация
- Production-ready из коробки (optimized builds, caching)

**vs Vite + React:**
- Vite быстрее в dev режиме, но Next.js - более полный фреймворк
- Next.js предоставляет SSR/SSG, file-based routing, оптимизации для production
- Vite требует дополнительной настройки для production deployment

### shadcn/ui

**Преимущества:**
- Компоненты **копируются в проект** - полный контроль над кодом
- Нет vendor lock-in - можно модифицировать компоненты как угодно
- Построен на Radix UI - accessibility (a11y) из коробки
- Темная/светлая тема поддерживается нативно через CSS variables
- Tailwind CSS базируется - consistency со стилями
- Минимальный bundle size - включаются только используемые компоненты
- Примеры dashboard в документации - быстрый старт

**vs Material-UI:**
- MUI тяжелее (~1MB+ bundle даже с tree-shaking)
- MUI имеет vendor lock-in - сложно кастомизировать глубоко
- shadcn/ui легче и современнее (CSS variables vs styled-components)

**vs Chakra UI:**
- Chakra использует CSS-in-JS (emotion) - runtime overhead
- shadcn/ui использует Tailwind - zero runtime, compile-time
- shadcn/ui дает больше контроля (компоненты в исходниках)

### pnpm

**Преимущества:**
- **Скорость установки**: в 2-3 раза быстрее npm (benchmark: 30 сек vs 90 сек)
- **Экономия места**: content-addressable storage - пакеты хранятся один раз (~50% меньше места)
- **Строгое управление peer dependencies**: меньше конфликтов версий
- **Монорепо поддержка**: workspaces для будущего расширения (dashboard + admin panel)
- **Безопасность**: strict node_modules structure предотвращает phantom dependencies

**vs npm:**
- npm медленнее и занимает больше места
- npm 7+ добавил workspaces, но pnpm все еще быстрее

**vs yarn:**
- Yarn 1 устарел
- Yarn 2+ (Berry) имеет Plug'n'Play, но менее совместим с экосистемой
- pnpm более предсказуем и активно развивается

### TypeScript strict mode

**Преимущества:**
- **Type safety с первого дня**: меньше багов в runtime
- **Улучшенное автодополнение** в IDE (VS Code, Cursor)
- **Самодокументирующийся код**: типы как документация
- **Легче рефакторинг**: IDE понимает структуру кода
- **noUncheckedIndexedAccess**: безопасность при работе с массивами и объектами

**Strict mode включает:**
- `strict: true` - все строгие проверки
- `noUncheckedIndexedAccess: true` - array[index] возвращает T | undefined
- `noImplicitAny` - запрет неявного any
- `strictNullChecks` - null/undefined строго типизированы

### Tailwind CSS

**Преимущества:**
- **Utility-first подход**: быстрая разработка без написания CSS
- **Минимум custom CSS**: консистентный дизайн через утилиты
- **Purging неиспользуемых стилей**: маленький bundle (~10KB после purge)
- **Responsive design из коробки**: префиксы sm:, md:, lg:, xl:
- **Отлично работает с shadcn/ui**: компоненты используют Tailwind классы
- **CSS variables для тем**: легкое переключение темной/светлой темы

**vs CSS Modules:**
- Tailwind быстрее для прототипирования
- Меньше контекстных переключений (не нужно переключаться между CSS/JS файлами)

**vs styled-components:**
- Tailwind zero runtime - все compile-time
- styled-components добавляет runtime overhead (~15KB)

## Альтернативы

### 1. Vite + React + Material-UI + npm

**Плюсы:**
- Vite очень быстрый dev server
- Material-UI зрелая библиотека с готовыми компонентами
- npm стандартный менеджер пакетов

**Минусы:**
- ❌ Нет SSR из коробки (нужен дополнительный setup)
- ❌ Material-UI тяжелый и сложно кастомизируется
- ❌ npm медленнее pnpm
- ❌ Требует больше настройки для production

### 2. Remix + Ant Design + yarn

**Плюсы:**
- Remix отличный фреймворк с фокусом на web standards
- Ant Design богатый набор компонентов

**Минусы:**
- ❌ Remix менее популярен чем Next.js (меньше примеров)
- ❌ Ant Design имеет специфичный дизайн (не минималистичный)
- ❌ yarn менее производителен чем pnpm

### 3. SvelteKit + custom components

**Плюсы:**
- Svelte компилирует в vanilla JS (маленький bundle)
- SvelteKit быстрый фреймворк

**Минусы:**
- ❌ Меньшая экосистема чем React
- ❌ Нужно писать компоненты с нуля
- ❌ Меньше примеров и туториалов

## Последствия

### Положительные:

- ✅ **Быстрый старт**: shadcn/ui примеры позволяют создать UI за часы
- ✅ **Отличная производительность**: Next.js оптимизации + Tailwind purging
- ✅ **Type safety**: TypeScript strict предотвращает ошибки
- ✅ **Легко расширять**: модульная архитектура готова к добавлению компонентов
- ✅ **Современный стек**: активное развитие всех технологий
- ✅ **Хороший DX**: быстрая установка (pnpm), hot reload, TypeScript
- ✅ **Production ready**: Next.js оптимизирован для деплоя

### Отрицательные:

- ⚠️ **Обучение Next.js 14**: App Router относительно новый (нужно изучать)
- ⚠️ **pnpm не везде**: некоторые CI/CD по умолчанию используют npm (но настраивается)
- ⚠️ **shadcn/ui копирует код**: компоненты в проекте (но это и плюс - контроль)

### Риски и митигация:

- **Риск:** Next.js 14 App Router может иметь breaking changes
  - *Митигация:* Используем stable release, следим за changelog, тестируем обновления

- **Риск:** Нужно кастомизировать shadcn/ui компоненты
  - *Митигация:* Компоненты в исходниках - легко модифицировать

- **Риск:** TypeScript strict может замедлить разработку
  - *Митигация:* Инвестиция в типы окупается меньшим количеством багов

## Заключение

Выбранный стек **Next.js 14 + shadcn/ui + pnpm + TypeScript strict + Tailwind CSS** оптимален по соотношению **скорость разработки / производительность / поддерживаемость** для MVP dashboard.

Стек позволяет:
- Создать MVP за несколько дней
- Обеспечить отличную производительность
- Легко расширять функционал
- Поддерживать качество кода (TypeScript, линтинг)

## Ссылки

- [Next.js Documentation](https://nextjs.org/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [pnpm Documentation](https://pnpm.io/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn/ui Dashboard Example](https://ui.shadcn.com/examples/dashboard)

