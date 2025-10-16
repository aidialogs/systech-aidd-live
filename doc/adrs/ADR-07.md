# ADR-07: Выбор технологического стека для Frontend

**Статус:** Принято  
**Дата:** 2025-10-16  
**Авторы:** systech-aidd team  
**Связанные ADR:** ADR-01, ADR-02, ADR-06

## Контекст

Для мониторинга активности AI-бота в Telegram необходим веб-интерфейс (дашборд статистики). Требования:

- **Современный UI/UX** - привлекательный и удобный интерфейс для визуализации метрик
- **Производительность** - быстрая загрузка и отзывчивость интерфейса
- **SEO-friendly** - возможность индексации для будущего публичного доступа
- **Type Safety** - строгая типизация как в backend (следование единому подходу)
- **Developer Experience** - удобство разработки и генерации кода с LLM
- **Интеграция с Backend** - простая интеграция с FastAPI backend через REST API
- **Accessibility** - доступность для пользователей с ограниченными возможностями
- **Responsive Design** - адаптивность под различные устройства

## Решение

Выбран стек: **Next.js 15 + React 19 + TypeScript + shadcn/ui + Tailwind CSS + pnpm**

## Обоснование выбора компонентов

### 1. Next.js 15 (Framework)

**Плюсы:**
- ✅ **SSR/SSG из коробки** - Server-Side Rendering и Static Site Generation для оптимальной производительности
- ✅ **App Router** - новая архитектура с React Server Components для лучшей производительности
- ✅ **Автоматическая оптимизация** - code splitting, image optimization, font optimization
- ✅ **TypeScript support** - первоклассная поддержка TypeScript
- ✅ **API Routes** - возможность создания backend endpoints (если потребуется)
- ✅ **Отличная документация** - comprehensive docs и активное сообщество
- ✅ **Production-ready** - используется крупными компаниями (Vercel, Netflix, Twitch)
- ✅ **LLM-friendly** - Claude и другие LLM отлично знают Next.js

**Минусы:**
- ⚠️ **Learning curve** - App Router - новая парадигма (требует изучения)
- ⚠️ **Breaking changes** - быстрое развитие может приводить к breaking changes

### 2. React 19 (UI Library)

**Плюсы:**
- ✅ **Индустриальный стандарт** - де-факто стандарт для построения современных UI
- ✅ **Огромная экосистема** - библиотеки, компоненты, инструменты
- ✅ **Декларативный подход** - легко читать и понимать код
- ✅ **Component-based** - переиспользуемые компоненты
- ✅ **LLM-friendly** - отлично знаком всем LLM для генерации кода
- ✅ **Hooks** - удобное управление состоянием без классов

**Минусы:**
- ⚠️ **Bundle size** - React runtime добавляет overhead (но Next.js оптимизирует)

### 3. TypeScript (Type Safety)

**Плюсы:**
- ✅ **Static typing** - предотвращение ошибок на этапе компиляции
- ✅ **IntelliSense** - автокомплит и подсказки в IDE
- ✅ **Рефакторинг** - безопасный рефакторинг с проверкой типов
- ✅ **Self-documenting code** - типы служат документацией
- ✅ **Соответствие backend** - единый подход к типизации (как в Python с type hints)
- ✅ **LLM-friendly** - LLM генерируют типизированный код

**Минусы:**
- ⚠️ **Initial overhead** - требуется время на описание типов
- ⚠️ **Learning curve** - для новичков может быть сложнее

### 4. shadcn/ui (UI Components)

**Плюсы:**
- ✅ **Не библиотека, а коллекция** - copy-paste компонентов в проект (полный контроль)
- ✅ **Кастомизация** - можно модифицировать компоненты под свои нужды
- ✅ **Radix UI под капотом** - accessibility из коробки (WCAG 2.1 AA)
- ✅ **Tailwind CSS стилизация** - легко изменять стили
- ✅ **Готовые блоки** - есть dashboard-01 блок (идеально для нашего кейса)
- ✅ **Меньший bundle** - включаются только используемые компоненты
- ✅ **Type-safe** - полная типизация TypeScript
- ✅ **Современный дизайн** - красивый и профессиональный вид

**Минусы:**
- ⚠️ **Ручное обновление** - обновления компонентов через copy-paste (решается версионированием в git)

### 5. Tailwind CSS (Styling)

**Плюсы:**
- ✅ **Utility-first** - быстрая разработка без написания CSS
- ✅ **Responsive design** - mobile-first подход из коробки
- ✅ **Tree-shaking** - неиспользуемые стили удаляются (минимальный bundle)
- ✅ **Consistency** - единообразный дизайн через design tokens
- ✅ **No naming conflicts** - нет проблем с именованием классов
- ✅ **Интеграция с shadcn/ui** - идеальное сочетание
- ✅ **Быстрое прототипирование** - легко экспериментировать с дизайном

**Минусы:**
- ⚠️ **Verbosity** - много классов в JSX (решается через компоненты)
- ⚠️ **Learning curve** - требуется привыкание к utility-first подходу

### 6. pnpm (Package Manager)

**Плюсы:**
- ✅ **Скорость** - значительно быстрее npm и yarn (symlink-based)
- ✅ **Экономия места** - content-addressable storage (одна версия пакета на диск)
- ✅ **Строгая изоляция** - предотвращает phantom dependencies
- ✅ **Монорепозитории** - отличная поддержка workspaces
- ✅ **Совместимость** - совместим с npm registry и package.json
- ✅ **Безопасность** - строгая проверка зависимостей

**Минусы:**
- ⚠️ **CI/CD настройка** - может потребовать дополнительной настройки (решается через corepack)

## Рассмотренные альтернативы

### 1. Vite + React Router vs Next.js

**Vite + React Router:**
- ✅ Быстрее в dev mode (HMR)
- ✅ Легче и проще для SPA
- ❌ Требует ручной настройки SSR
- ❌ Нет встроенной оптимизации (image, font, etc.)
- ❌ Нужна ручная настройка routing, SEO

**Вердикт:** Next.js предоставляет больше из коробки. Для dashboard с потенциальным SEO и возможным масштабированием Next.js лучший выбор.

### 2. Material-UI / Ant Design vs shadcn/ui

**Material-UI:**
- ✅ Готовая библиотека с множеством компонентов
- ✅ Material Design система
- ❌ Фиксированный стиль (сложнее кастомизация)
- ❌ Больший bundle size
- ❌ Зависимость от версий библиотеки

**Ant Design:**
- ✅ Богатая библиотека компонентов
- ✅ Enterprise-ready
- ❌ Специфичный дизайн (для enterprise apps)
- ❌ Большой bundle size
- ❌ Меньшая гибкость в кастомизации

**Вердикт:** shadcn/ui дает полный контроль над компонентами и стилями, меньший bundle size, легче кастомизация под дизайн проекта.

### 3. CSS Modules / Styled Components vs Tailwind CSS

**CSS Modules:**
- ✅ Scoped styles
- ✅ Привычный CSS синтаксис
- ❌ Больше boilerplate (отдельные файлы)
- ❌ Нет utility-first преимуществ

**Styled Components:**
- ✅ CSS-in-JS с props
- ✅ Dynamic styling
- ❌ Runtime overhead
- ❌ Bundle size увеличивается
- ❌ Сложнее для SSR

**Вердикт:** Tailwind CSS быстрее для прототипирования, меньше boilerplate, нет runtime overhead, идеальная интеграция с shadcn/ui.

### 4. npm / yarn vs pnpm

**npm:**
- ✅ Стандартный менеджер
- ✅ Широкая поддержка
- ❌ Медленнее установка
- ❌ Занимает больше места
- ❌ Phantom dependencies

**yarn v1:**
- ✅ Быстрее npm
- ✅ Deterministic installs
- ❌ Устарел (больше не развивается)

**yarn v2+ (berry):**
- ✅ PnP (Plug'n'Play)
- ✅ Современная архитектура
- ❌ Сложнее в настройке
- ❌ Compatibility issues

**Вердикт:** pnpm современнее, быстрее, эффективнее. Строгая изоляция предотвращает проблемы с зависимостями.

## Последствия

### Положительные

✅ **Быстрая разработка** - готовые компоненты shadcn/ui ускоряют разработку  
✅ **Отличная производительность** - Next.js SSR/SSG обеспечивают быструю загрузку  
✅ **Type safety** - TypeScript снижает количество ошибок на 30-40%  
✅ **Accessibility** - Radix UI обеспечивает WCAG 2.1 AA compliance  
✅ **Отличная документация** - все инструменты имеют качественную документацию  
✅ **LLM-friendly stack** - Claude и другие LLM отлично знают все компоненты  
✅ **Единый подход** - type safety как в backend (Python type hints = TypeScript)  
✅ **Production-ready** - все компоненты стека проверены в production  
✅ **SEO-friendly** - Next.js SSR обеспечивает хорошую индексацию  

### Отрицательные

⚠️ **Learning curve** - Next.js App Router требует изучения (новая парадигма)  
⚠️ **CI/CD настройка** - pnpm может потребовать дополнительной настройки  
⚠️ **Tailwind verbosity** - много классов в JSX (решается через компоненты)  
⚠️ **shadcn/ui updates** - компоненты требуют ручного обновления  

### Риски и митигация

| Риск | Вероятность | Воздействие | Митигация |
|------|-------------|-------------|-----------|
| Breaking changes в Next.js | Средняя | Среднее | Фиксация версий, осторожные обновления, чтение changelog |
| pnpm issues в CI/CD | Низкая | Низкое | Использование corepack, документирование настройки |
| shadcn/ui компоненты устаревают | Низкая | Низкое | Версионирование в git, периодический audit |
| Tailwind сложность для команды | Низкая | Низкое | Обучение, best practices, компонентный подход |

## Требования к окружению

**Development:**
- Node.js 18+ (LTS)
- pnpm 9+
- VSCode с расширениями: TypeScript, Prettier, ESLint, Tailwind IntelliSense

**Production:**
- Node.js 18+ runtime
- Static hosting (Vercel, Netlify, Cloudflare Pages) или
- Self-hosted (Docker container с Node.js)

## Принципы архитектуры

Следуя backend vision, применяем те же принципы к frontend:

- **KISS (Keep It Simple, Stupid)** - никакого оверинжиниринга
- **Type Safety First** - строгая типизация всего кода
- **Component-First** - переиспользуемые компоненты
- **Accessibility First** - WCAG 2.1 AA compliance
- **Mobile First** - responsive design
- **Server Components First** - использовать RSC где возможно

## Интеграция с Backend

- **API endpoint**: `http://localhost:8000/api/stats`
- **CORS**: уже настроен в FastAPI backend для `http://localhost:3000`
- **Protocol**: REST API с JSON
- **Type safety**: TypeScript interfaces на основе OpenAPI schema

## Следующие шаги

После принятия ADR:
1. ✅ Создать техническое видение frontend (front-vision.md)
2. ✅ Инициализировать Next.js проект с выбранным стеком
3. ✅ Настроить инструменты разработки (ESLint, Prettier, TypeScript strict)
4. ✅ Настроить shadcn/ui и добавить базовые компоненты
5. ✅ Создать структуру проекта и базовые файлы

## Ссылки

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [pnpm Documentation](https://pnpm.io)
- [Radix UI Documentation](https://www.radix-ui.com)

## Обновления

- **2025-10-16**: Первая версия - Sprint S2

