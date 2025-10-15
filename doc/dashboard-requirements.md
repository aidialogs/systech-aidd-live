# Dashboard Requirements

> Техническое видение бота: @vision.md  
> План разработки дашборда: @dashboard-tasklist.md

---

## Визуальный стиль

**Дизайн:** темная тема в стиле [shadcn/ui dashboard](https://ui.shadcn.com/examples/dashboard)

- Темный фон (dark mode)
- Современные карточки с тенями
- Минималистичный UI
- Responsive layout

---

## Компоненты дашборда

### 1. Overview Cards

**4 карточки метрик в ряд:**

| Метрика | Описание |
|---------|----------|
| Total Users | Общее количество уникальных пользователей |
| Total Conversations | Общее количество активных диалогов |
| Total Messages | Общее количество сообщений (user + assistant) |
| Avg Conversation Length | Средняя длина диалога в сообщениях |

**Каждая карточка содержит:**
- Название метрики
- Значение (число)
- Тренд (процент изменения)
- Стрелка направления (↑ вверх / ↓ вниз)
- Подпись (например "Trending up this month")

**Пример карточки:**
```
Total Revenue
$1,250.00
↑ +12.5%
Trending up this month
```

---

### 2. Message Activity Graph

**График количества сообщений по времени**

- **Тип:** Line chart с областью (area chart)
- **Заголовок:** "Message Activity" 
- **Подзаголовок:** "Total messages for the selected period"
- **Фильтры периода:** 
  - Last 7 days
  - Last 30 days
- **Оси:**
  - X: дата/время
  - Y: количество сообщений
- **Стиль:** плавная линия с градиентной заливкой

---

## REST API

### Endpoint

```
GET /api/stats
```

### Формат ответа

```json
{
  "overview": {
    "total_users": {
      "value": 150,
      "trend": 12.5,
      "trend_direction": "up"
    },
    "total_conversations": {
      "value": 234,
      "trend": -5.2,
      "trend_direction": "down"
    },
    "total_messages": {
      "value": 3420,
      "trend": 8.3,
      "trend_direction": "up"
    },
    "avg_conversation_length": {
      "value": 14.6,
      "trend": 2.1,
      "trend_direction": "up"
    }
  },
  "message_activity": {
    "time_range": "7d",
    "data_points": [
      {
        "timestamp": "2025-10-15T00:00:00Z",
        "message_count": 45
      },
      {
        "timestamp": "2025-10-16T00:00:00Z",
        "message_count": 52
      }
    ]
  }
}
```

### Структура данных

**overview:**
- `value`: текущее значение метрики
- `trend`: процент изменения
- `trend_direction`: `"up"` | `"down"` | `"neutral"`

**message_activity:**
- `time_range`: выбранный период (`"7d"` | `"30d"`)
- `data_points`: массив точек для графика
  - `timestamp`: ISO 8601 формат (UTC)
  - `message_count`: количество сообщений

---

## Технические требования

### Frontend
- **Framework:** Next.js 14+ (App Router)
- **UI Components:** shadcn/ui
- **Styling:** Tailwind CSS
- **Charts:** shadcn/ui charts (recharts)
- **TypeScript:** strict mode

### Backend
- **Framework:** FastAPI
- **Endpoint:** `GET /api/stats`
- **CORS:** разрешен для localhost:3000
- **Формат дат:** ISO 8601 (UTC)

### MVP ограничения
- ✅ Только чтение данных
- ✅ Без авторизации
- ✅ Локальный запуск
- ✅ In-memory данные (теряются при перезапуске)
- ❌ Без персистентного хранилища
- ❌ Без real-time updates

---

## Источник данных

**ContextManager** (in-memory):
- Данные: `dict[tuple[int, int], list[Message]]`
- Ключ: `(user_id, chat_id)`
- Значение: список сообщений диалога

**Что нужно добавить:**
- Timestamp к каждому `Message` для построения графика
- Агрегация метрик из ContextManager
