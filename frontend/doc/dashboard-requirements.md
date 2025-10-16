# Dashboard Requirements

## Обзор

Дашборд статистики для мониторинга активности AI-бота в Telegram. Основан на референсе [shadcn/ui dashboard-01](https://ui.shadcn.com/blocks#dashboard-01) с адаптацией под специфику нашего проекта.

## Референсы

- **UI Design**: [shadcn/ui dashboard-01](https://ui.shadcn.com/blocks#dashboard-01)
- **Visual Reference**: [front-reference.png](./front-reference.png)

## Метрики дашборда

### 4 карточки метрик

#### 1. Total Users
- **Значение**: Общее количество зарегистрированных пользователей
- **Тренд**: Изменение за последние 30 дней (%)
- **Описание**: Total registered users
- **Источник данных**: Таблица `users` (количество записей с `is_deleted = false`)

#### 2. Active Dialogs
- **Значение**: Количество уникальных активных диалогов
- **Тренд**: Изменение за последние 30 дней (%)
- **Описание**: Unique active conversations
- **Источник данных**: Уникальные пары `(user_id, chat_id)` в таблице `messages`

#### 3. Total Messages
- **Значение**: Общее количество сообщений
- **Тренд**: Изменение за последние 30 дней (%)
- **Описание**: All messages exchanged
- **Источник данных**: Таблица `messages` (количество записей с `is_deleted = false`)

#### 4. Avg Message Length
- **Значение**: Средняя длина сообщения (в символах)
- **Тренд**: Изменение за последние 30 дней (%)
- **Описание**: Average characters per message
- **Источник данных**: `AVG(content_length)` из таблицы `messages`

### График Messages Over Time

- **Тип**: Area/Line chart с временным рядом
- **Данные**: Количество сообщений по дням
- **Периоды**: 
  - Last 7 days (7 точек данных)
  - Last 30 days (30 точек данных)
- **Переключение**: Кнопки-переключатели для выбора периода
- **Формат даты**: ISO 8601 UTC (`2025-01-05T00:00:00Z`)
- **Источник данных**: Агрегация по дням из таблицы `messages`

## Layout структура

На основе референса shadcn/ui dashboard-01:

```
┌─────────────────────────────────────────────────────────┐
│ Header (Navigation, Title, User Menu)                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │  Total   │  │  Active  │  │  Total   │  │   Avg   │ │
│  │  Users   │  │ Dialogs  │  │ Messages │  │ Message │ │
│  │          │  │          │  │          │  │  Length │ │
│  │  1,234   │  │   456    │  │  45,678  │  │   127   │ │
│  │ +12.5%   │  │  +8.3%   │  │ +15.2%   │  │  -2.1%  │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Messages Over Time                  [7d] [30d]    │ │
│  │                                                    │ │
│  │     ╱╲    ╱╲                                      │ │
│  │    ╱  ╲  ╱  ╲╱╲                                   │ │
│  │   ╱    ╲╱      ╲  ╱╲                              │ │
│  │  ╱              ╲╱  ╲                             │ │
│  │ ─────────────────────────────────────────────────  │ │
│  │ Jan 10  Jan 11  Jan 12  Jan 13  Jan 14  Jan 15    │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## UI компоненты

### MetricCard компонент
- **Title**: Название метрики
- **Value**: Основное значение (форматированное с разделителями тысяч)
- **Trend**: Процент изменения с иконкой (↑ для роста, ↓ для падения)
- **Description**: Краткое описание метрики
- **Цвет тренда**: 
  - Зелёный для положительного тренда
  - Красный для отрицательного тренда

### Chart компонент
- **Title**: "Messages Over Time"
- **Period Switcher**: Кнопки для выбора периода (7d / 30d)
- **Chart Type**: Area chart или Line chart
- **Tooltip**: Показывать точное значение при наведении
- **Responsive**: Адаптивный размер под разные экраны

## API контракт

### Endpoint: GET /api/stats

**Response format:**

```typescript
interface MetricCard {
  title: string;
  value: string;
  trend: string;        // "+12.5%", "-20%", etc
  description: string;
}

interface ChartDataPoint {
  date: string;         // ISO 8601 UTC: "2025-01-05T00:00:00Z"
  value: number;
}

interface DashboardStats {
  total_users: MetricCard;
  active_dialogs: MetricCard;
  total_messages: MetricCard;
  avg_message_length: MetricCard;
  messages_chart_7d: ChartDataPoint[];   // 7 элементов
  messages_chart_30d: ChartDataPoint[];  // 30 элементов
}
```

**Example Response:**

```json
{
  "total_users": {
    "title": "Total Users",
    "value": "1,234",
    "trend": "+12.5%",
    "description": "Total registered users"
  },
  "active_dialogs": {
    "title": "Active Dialogs",
    "value": "456",
    "trend": "+8.3%",
    "description": "Unique active conversations"
  },
  "total_messages": {
    "title": "Total Messages",
    "value": "45,678",
    "trend": "+15.2%",
    "description": "All messages exchanged"
  },
  "avg_message_length": {
    "title": "Avg Message Length",
    "value": "127",
    "trend": "-2.1%",
    "description": "Average characters per message"
  },
  "messages_chart_7d": [
    {"date": "2025-01-10T00:00:00Z", "value": 1234},
    {"date": "2025-01-11T00:00:00Z", "value": 1456},
    {"date": "2025-01-12T00:00:00Z", "value": 1389},
    {"date": "2025-01-13T00:00:00Z", "value": 1567},
    {"date": "2025-01-14T00:00:00Z", "value": 1423},
    {"date": "2025-01-15T00:00:00Z", "value": 1678},
    {"date": "2025-01-16T00:00:00Z", "value": 1789}
  ],
  "messages_chart_30d": [
    {"date": "2024-12-18T00:00:00Z", "value": 1100},
    {"date": "2024-12-19T00:00:00Z", "value": 1150},
    ...
    {"date": "2025-01-16T00:00:00Z", "value": 1789}
  ]
}
```

## Технические требования

### Frontend
- **Framework**: TBD (будет определён в Sprint 2)
- **UI Library**: shadcn/ui компоненты
- **Charts**: TBD (recharts, visx или аналог)
- **HTTP Client**: fetch API или axios
- **Responsive**: Mobile-first подход

### Backend (Mock API)
- **Framework**: FastAPI
- **Port**: 8000
- **CORS**: Разрешить `http://localhost:3000`
- **Format**: JSON
- **Documentation**: Swagger UI на `/docs`

## UX принципы

1. **Instant Feedback**: Быстрая загрузка и отображение данных
2. **Clear Trends**: Понятная визуализация изменений
3. **Responsive Design**: Работает на всех устройствах
4. **Accessibility**: Поддержка screen readers
5. **Loading States**: Показывать скелетон при загрузке
6. **Error Handling**: Понятные сообщения об ошибках

## Будущие улучшения (не в текущей итерации)

- Фильтрация по датам (custom date range)
- Экспорт данных в CSV/Excel
- Real-time обновление через WebSocket
- Drill-down в детали метрик
- Сравнение периодов (compare previous period)
- Дополнительные метрики (average response time, most active users, etc.)

---

**Версия документа**: 1.0  
**Дата создания**: 2025-10-16  
**Статус**: Активные требования для Sprint 1

