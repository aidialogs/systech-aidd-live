# ADR-07: Выбор технологического стека для Frontend

**Дата**: 2025-10-17  
**Статус**: Принято  
**Контекст**: Sprint S2 - Инициализация Frontend проекта

---

## Контекст

Для реализации веб-интерфейса проекта (дашборд статистики и админ-чат) необходимо выбрать современный и эффективный технологический стек. 

Требования:
- Быстрая разработка UI компонентов
- Интеграция с Backend API (FastAPI)
- Поддержка темной/светлой темы
- Type safety на уровне backend (TypeScript ↔ Python type hints)
- Высокая производительность и SEO
- Масштабируемость архитектуры
- Соответствие best practices 2025 года

---

## Рассмотренные варианты

### 1. Framework

**Варианты:**

a) **Next.js 15 (App Router)** ✅
   - Server Components по умолчанию
   - File-based routing
   - Встроенная оптимизация (images, fonts, code splitting)
   - SEO-friendly из коробки
   - Отличная документация и community
   - Рекомендуется React team

b) **Next.js (Pages Router)**
   - Старый подход, но проверенный временем
   - Проще для новичков
   - Меньше возможностей оптимизации
   - Не рекомендуется для новых проектов в 2025

c) **Remix**
   - Современный подход с фокусом на web standards
   - Хороший DX
   - Меньшая экосистема по сравнению с Next.js
   - Сложнее интеграция с некоторыми библиотеками

d) **Vite + React**
   - Максимальная гибкость
   - Быстрая сборка
   - Требует настройки routing, SSR, оптимизаций вручную
   - Больше работы на начальном этапе

**Решение**: Next.js 15 с App Router

**Обоснование**:
- Server Components дают лучшую производительность
- Встроенные оптимизации (не нужны дополнительные инструменты)
- Идеальная интеграция с React и TypeScript
- Большая экосистема и активная поддержка
- SEO из коробки (важно для будущего)

---

### 2. Язык

**Варианты:**

a) **TypeScript** ✅
   - Строгая типизация
   - Раннее обнаружение ошибок
   - Лучший DX (автокомплит, refactoring)
   - Стандарт индустрии в 2025

b) **JavaScript**
   - Проще для начинающих
   - Меньше boilerplate
   - Отсутствие type safety
   - Больше runtime ошибок

**Решение**: TypeScript 5+

**Обоснование**:
- Соответствие подходу backend (Python + mypy strict)
- Type safety на уровне компиляции
- Лучшая интеграция с Next.js и современными библиотеками
- Самодокументирующийся код
- Легче рефакторинг при росте проекта

---

### 3. UI Library

**Варианты:**

a) **shadcn/ui** ✅
   - Копируемые компоненты (не npm пакет)
   - Полный контроль над кодом
   - Базируется на Radix UI (accessibility)
   - Высокое качество и современный дизайн
   - TypeScript из коробки
   - Поддержка тем через CSS variables

b) **Material-UI (MUI)**
   - Огромная библиотека компонентов
   - Хорошая документация
   - Тяжелый bundle size
   - Сложная кастомизация
   - Специфичный Material Design стиль

c) **Chakra UI**
   - Простота использования
   - Хорошая accessibility
   - Меньше компонентов чем MUI
   - Менее активная разработка в последнее время

d) **Ant Design**
   - Много компонентов из коробки
   - Хорош для enterprise приложений
   - Специфичный дизайн (сложно адаптировать)
   - Большой bundle size

**Решение**: shadcn/ui

**Обоснование**:
- Полный контроль: код копируется в проект, можно модифицировать
- Минимальный bundle: только те компоненты, которые используются
- Radix UI primitives: accessibility из коробки
- Tailwind CSS integration: консистентность стилей
- Flexibility: легко адаптировать под наш дизайн
- Modern: соответствует трендам 2025 года

---

### 4. Styling

**Варианты:**

a) **Tailwind CSS** ✅
   - Utility-first подход
   - Быстрая разработка
   - Консистентный дизайн через design tokens
   - Excellent tree-shaking (минимальный CSS)
   - Отличная экосистема и plugins
   - Темы через CSS variables

b) **CSS Modules**
   - Изоляция стилей
   - Привычный CSS синтаксис
   - Больше boilerplate
   - Меньше переиспользования

c) **Styled Components**
   - CSS-in-JS
   - Dynamic styling
   - Runtime overhead
   - Проблемы с Server Components

**Решение**: Tailwind CSS

**Обоснование**:
- Идеальная интеграция с Next.js и shadcn/ui
- Быстрая разработка без переключения между файлами
- Design system из коробки (spacing, colors, typography)
- Отличная производительность (нет runtime CSS-in-JS)
- Легко поддерживать dark/light темы
- JIT mode: генерация только используемых классов

---

### 5. Пакетный менеджер

**Варианты:**

a) **pnpm** ✅
   - Fastest: быстрее npm и yarn
   - Disk efficient: symlinks вместо копирования
   - Strict: строгая изоляция зависимостей
   - Monorepo friendly
   - Полная совместимость с npm

b) **npm**
   - Встроен в Node.js
   - Самый распространенный
   - Медленнее pnpm
   - Занимает больше места на диске

c) **yarn**
   - Быстрее npm (но медленнее pnpm)
   - Workspaces для монорепозиториев
   - Меньшее community по сравнению с npm/pnpm

**Решение**: pnpm

**Обоснование**:
- Скорость: значительно быстрее установка зависимостей
- Эффективность: экономит место на диске (symlinks)
- Безопасность: строгая изоляция предотвращает phantom dependencies
- Современность: рекомендуется для новых проектов в 2025
- Совместимость: работает со всеми npm пакетами

---

### 6. Charts библиотека (предварительный выбор для Sprint S3)

**Варианты:**

a) **shadcn/ui charts** ✅ (предварительно)
   - Обертка над Recharts с shadcn/ui стилями
   - Единообразие с остальными компонентами
   - TypeScript типизация
   - Поддержка тем из коробки
   - Копируемые компоненты (можно кастомизировать)

b) **Recharts**
   - Популярная React charting библиотека
   - Declarative API
   - Хорошая документация
   - Нужна кастомизация для shadcn/ui стиля

c) **Chart.js + react-chartjs-2**
   - Очень популярная (не только React)
   - Imperative API (сложнее с React)
   - Много типов графиков
   - Менее React-идиоматичная

d) **Tremor**
   - Специально для дашбордов
   - Базируется на Recharts и Tailwind
   - Меньше гибкости
   - Более опinionated

**Предварительное решение**: shadcn/ui charts

**Обоснование**:
- Консистентность: единый стиль с shadcn/ui компонентами
- Темы: автоматическая поддержка dark/light
- Контроль: копируемые компоненты, можно модифицировать
- DX: отличная типизация и документация
- **Примечание**: финальное решение будет принято в Sprint S3 после детального анализа требований к визуализации данных

---

## Итоговое решение

### Выбранный стек

- **Framework**: Next.js 15+ (App Router)
- **Language**: TypeScript 5+
- **UI Library**: shadcn/ui
- **Styling**: Tailwind CSS
- **Package Manager**: pnpm
- **Icons**: lucide-react (используется shadcn/ui)
- **Themes**: next-themes
- **HTTP Client**: native fetch (Next.js)
- **Charts** (предварительно): shadcn/ui charts

### Дополнительные инструменты

- **Linting**: ESLint (next/core-web-vitals, next/typescript)
- **Formatting**: Prettier
- **Type Checking**: TypeScript strict mode
- **Dev Tools**: Next.js DevTools, React DevTools

---

## Последствия

### Положительные

✅ **Производительность**:
- Server Components = меньше JavaScript в браузере
- Автоматическая оптимизация images, fonts, code splitting
- Fast Refresh для быстрой разработки

✅ **Developer Experience**:
- TypeScript strict mode = меньше runtime ошибок
- Отличная документация Next.js, shadcn/ui, Tailwind
- Быстрая установка зависимостей (pnpm)
- Автоматические проверки качества (ESLint, Prettier, tsc)

✅ **Масштабируемость**:
- Модульная архитектура (компонентный подход)
- Легко добавлять новые features
- Хорошая структура проекта

✅ **Поддержка**:
- Все инструменты активно развиваются
- Большое community и экосистема
- Регулярные обновления и security patches

✅ **Соответствие Backend подходу**:
- TypeScript strict ↔ Python mypy strict
- ESLint + Prettier ↔ ruff
- Type-safe API integration
- Аналогичная философия quality checks

### Негативные

⚠️ **Требования**:
- Node.js 18+ required
- Знание TypeScript необходимо
- Необходимость изучения Next.js App Router (новый подход)

⚠️ **Зависимости**:
- Минимальные, но есть: React, Next.js, Tailwind
- pnpm не так распространен как npm (но совместим)

⚠️ **Complexity**:
- Server vs Client Components требует понимания
- shadcn/ui компоненты нужно копировать (не npm install)

### Риски и митигация

**Риск 1**: Быстрое развитие Next.js может привести к breaking changes
- **Митигация**: Фиксация версий в package.json, осторожные обновления

**Риск 2**: shadcn/ui компоненты требуют копирования и обновления вручную
- **Митигация**: Версионирование в git, аккуратные обновления только при необходимости

**Риск 3**: pnpm менее знаком разработчикам
- **Митигация**: Документация в README, полная совместимость с npm командами

---

## Альтернативы (не выбраны)

### Почему НЕ Remix

- Меньшая экосистема по сравнению с Next.js
- Сложнее найти ready-to-use решения
- Next.js имеет лучшую интеграцию с Vercel (если понадобится деплой)

### Почему НЕ Material-UI

- Тяжелый bundle size (важно для performance)
- Специфичный Material Design стиль (сложно кастомизировать)
- shadcn/ui дает больше контроля при меньшем весе

### Почему НЕ CSS Modules / Styled Components

- Tailwind быстрее для разработки
- Лучшая интеграция с shadcn/ui
- Нет runtime overhead (в отличие от CSS-in-JS)

---

## Ссылки

- [Next.js Documentation](https://nextjs.org/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
- [pnpm Documentation](https://pnpm.io)
- [Frontend Vision](../../frontend/doc/frontend-vision.md)
- [Frontend Roadmap](../../frontend/doc/frontend-roadmap.md)

---

## История изменений

| Дата | Изменение | Автор |
|------|-----------|-------|
| 2025-10-17 | Initial version - выбор стека для Sprint S2 | AI Agent |

---

