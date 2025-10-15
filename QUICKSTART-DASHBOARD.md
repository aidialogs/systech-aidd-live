# Quick Start: Dashboard

> Быстрый запуск frontend dashboard для визуализации статистики бота

---

## 🚀 Первый запуск

### 1. Установка зависимостей

```bash
make dashboard-install
```

### 2. Конфигурация

Создайте файл `.env.local` в директории `dashboard/`:

```bash
cd dashboard
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

Или создайте вручную файл `dashboard/.env.local` со следующим содержимым:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Запуск

**Вариант A: Запуск всего вместе (рекомендуется)**

```bash
make dev-all
```

Это запустит:
- Backend API на `http://localhost:8000`
- Frontend Dashboard на `http://localhost:3000`

**Вариант B: Раздельный запуск**

В первом терминале запустите API:
```bash
make run-api
```

Во втором терминале запустите Dashboard:
```bash
make dashboard-dev
```

---

## 📋 Доступные команды

### Разработка

| Команда | Описание |
|---------|----------|
| `make dashboard-dev` | Запуск dev сервера (http://localhost:3000) |
| `make dashboard-build` | Production сборка |
| `make dashboard-start` | Запуск production сервера |
| `make dev-all` | Запуск Backend + Frontend одновременно |

### Проверка качества

| Команда | Описание |
|---------|----------|
| `make dashboard-lint` | ESLint проверка |
| `make dashboard-type-check` | TypeScript проверка типов |
| `make dashboard-check` | Полная проверка (type-check + lint + build) |

### Утилиты

| Команда | Описание |
|---------|----------|
| `make dashboard-install` | Установка зависимостей (pnpm install) |
| `make dashboard-clean` | Очистка .next, node_modules |

---

## 🔍 Проверка перед коммитом

Запустите полную проверку:

```bash
make dashboard-check
```

Эта команда выполнит:
1. ✅ TypeScript type-check
2. ✅ ESLint проверку
3. ✅ Production сборку

Все проверки должны пройти без ошибок!

---

## 🛠️ Разработка компонентов

### Структура проекта

```
dashboard/
├── app/              # Next.js pages (App Router)
├── components/       # React компоненты
│   ├── ui/          # shadcn/ui компоненты
│   └── *.tsx        # кастомные компоненты
├── lib/             # утилиты и API клиент
├── types/           # TypeScript интерфейсы
└── public/          # статические файлы
```

### Добавление shadcn/ui компонента

```bash
cd dashboard
pnpm dlx shadcn@latest add <component-name>
```

Примеры:
```bash
pnpm dlx shadcn@latest add button
pnpm dlx shadcn@latest add card
pnpm dlx shadcn@latest add table
```

### Правила разработки

- ✅ Один компонент = один файл
- ✅ TypeScript strict mode
- ✅ Все props типизированы
- ✅ Используем Tailwind CSS
- ✅ Loading и error states обязательны

См. полные правила: `.cursor/rules/conventions-front.mdc`

---

## 📖 Документация

- **Техническое видение**: `dashboard/doc/front-vision.md`
- **ADR стека**: `doc/adrs/ADR-06.md`
- **План разработки**: `doc/dashboard-tasklist.md`
- **Правила разработки**: `.cursor/rules/conventions-front.mdc`

---

## 🐛 Troubleshooting

### Dashboard не подключается к API

Проверьте:
1. API запущен: `curl http://localhost:8000/health`
2. CORS настроен (должен быть разрешен localhost)
3. `.env.local` содержит правильный `NEXT_PUBLIC_API_URL`

### TypeScript ошибки

```bash
make dashboard-type-check
```

Исправьте все ошибки типизации перед продолжением.

### Ошибки линтера

```bash
make dashboard-lint
```

Следуйте рекомендациям ESLint.

### Очистка кеша

```bash
make dashboard-clean
make dashboard-install
```

---

## ✅ Реализованные Итерации

### Итерация 7: ✅ Завершено - Интеграция с API

Frontend Dashboard подключен к реальному backend API:

**Что реализовано:**
- ✅ Custom hook `useStats()` для загрузки данных из API
- ✅ Компоненты `LoadingSkeleton` и `ErrorMessage`
- ✅ `SectionCards` получает данные из API (overview метрики)
- ✅ `ChartAreaInteractive` получает данные из API (message_activity)
- ✅ Обработка состояний: loading, error, success
- ✅ Retry функциональность при ошибках
- ✅ TypeScript strict mode без ошибок
- ✅ Адаптивный дизайн сохранен

**Как протестировать:**

1. Запустите Backend API:
   ```bash
   make run-api
   # API запустится на http://localhost:8000
   ```

2. В отдельном терминале запустите Dashboard:
   ```bash
   make dashboard-dev
   # Dashboard на http://localhost:3000
   ```

3. Откройте http://localhost:3000/dashboard

4. Проверьте:
   - Dashboard загружается с loading skeleton
   - Отображаются реальные метрики из API
   - График показывает данные message_activity
   - Остановите API и обновите страницу → должно появиться сообщение об ошибке с кнопкой Retry
   - Запустите API снова и нажмите Retry → данные загрузятся

5. Проверьте API напрямую:
   ```bash
   curl http://localhost:8000/api/stats | jq
   ```

### Итерация 5-6: ✅ Завершено - Dashboard UI

Dashboard UI реализован с использованием shadcn/ui:

**Что реализовано:**
- ✅ 4 карточки метрик с трендами
- ✅ График активности сообщений с фильтрами 7d/30d
- ✅ Темная тема по умолчанию с переключателем
- ✅ Адаптивный layout (mobile/tablet/desktop)
- ✅ TypeScript strict mode

## ✨ Следующие шаги

1. ✅ Итерация 5: Базовая структура UI - **Завершено**
2. ✅ Итерация 6: Реализация Dashboard страницы - **Завершено**
3. ✅ Итерация 7: Интеграция с реальным API - **Завершено**
4. ⏳ Итерация 8: Финальное тестирование

См. план: `doc/dashboard-tasklist.md`

