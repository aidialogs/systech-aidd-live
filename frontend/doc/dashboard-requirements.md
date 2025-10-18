# Dashboard Requirements - Sprint S3

## Обзор

Дашборд статистики диалогов предоставляет визуальную аналитику работы чат-бота.

## Функциональные требования

### FR-1: Карточки метрик (Overview)
- Отображение 4 карточек с ключевыми метриками:
  - Total Messages - общее количество сообщений
  - Total Users - количество пользователей
  - Active Chats - количество активных чатов
  - Avg Message Length - средняя длина сообщения
- Цветные иконки для каждой метрики
- Форматирование чисел с разделителями (toLocaleString)

### FR-2: График сообщений по времени
- Area chart с градиентной заливкой
- Адаптивное форматирование оси X в зависимости от периода:
  - day: почасовая разбивка (HH:MM)
  - week: дневная разбивка (MM-DD)
  - month: дневная разбивка (MM-DD)
  - all: месячная разбивка (YYYY-MM)
- Tooltip с детальной информацией при наведении

### FR-3: График распределения по ролям
- Bar chart с 3 столбцами: User, Assistant, System
- Цветовая дифференциация (chart-2, chart-3, chart-4)
- Отображение точных значений в tooltip

### FR-4: Карточка топовых метрик
- 4 метрики в вертикальном списке с разделителями:
  - Most Active Users
  - Messages Today
  - Messages This Week
  - Messages This Month
- Цветные значения для визуального акцента

### FR-5: Фильтрация по периодам
- Выпадающий список (Select) с 4 опциями:
  - Last 24 Hours (day)
  - Last 7 Days (week)
  - Last 30 Days (month)
  - All Time (all)
- Автоматическое обновление всех компонентов при изменении периода

### FR-6: Обработка состояний
- Loading state: центрированное сообщение "Loading statistics..."
- Error state: сообщение об ошибке с инструкцией проверить API
- Empty state: не требуется (Mock API всегда возвращает данные)

## Нефункциональные требования

### NFR-1: Адаптивный дизайн
- Mobile (<768px): стек в 1 колонку
- Tablet (768-1023px): карточки в 2 колонки, графики в 1 колонку
- Desktop (≥1024px): карточки в 4 колонки, графики в 2 колонки

### NFR-2: Цветовая схема
- Яркие, насыщенные цвета (не блеклые)
- Поддержка dark/light режимов
- Градиенты на графиках для визуальной привлекательности

### NFR-3: Производительность
- Загрузка данных через fetch с cache: 'no-store'
- Отображение loading state до получения данных
- Минимизация rerenders через правильное использование useEffect

### NFR-4: Типизация
- Полная TypeScript типизация всех компонентов
- Использование интерфейсов из lib/types.ts
- Props interfaces для всех компонентов

## Технические детали

### API Integration
- Endpoint: GET /api/v1/statistics?period={day|week|month|all}
- Function: getStatistics(period) из lib/api.ts
- Response type: Statistics interface

### Компоненты
- PeriodSelector - выбор периода
- StatsCards - карточки overview
- MessagesOverTimeChart - график по времени
- MessagesByRoleChart - график по ролям
- TopMetricsCard - топовые метрики
- Dashboard Page - главная страница с композицией всех компонентов

### Зависимости
- recharts - библиотека графиков
- shadcn/ui chart - обертка с темизацией
- Существующие shadcn/ui компоненты (Card, Select, etc.)

