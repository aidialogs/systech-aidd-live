<!-- 844754ba-0ea5-437f-bf0e-16082d148c1c 58202189-8283-43c9-a52e-21ad5c7168a2 -->
# Итерация 1: Анализ требований и проектирование API

## Цель

Создать лаконичный документ с требованиями к дашборду и спецификацией API endpoint.

## Компоненты дашборда

1. **Overview Cards** - 4 карточки с метриками и трендами
2. **Message Activity Graph** - график количества сообщений по дням

Дизайн: темная тема как в [shadcn/ui dashboard](https://ui.shadcn.com/examples/dashboard)

## Документ требований

Создать `doc/dashboard-requirements.md` с описанием:

**UI компоненты:**

- 4 карточки метрик (Total Users, Total Conversations, Total Messages, Avg Conversation Length)
- Каждая карточка: значение, тренд (%), стрелка вверх/вниз
- График активности: line chart с фильтрами периода (Last 7 days, Last 30 days)

**Технические требования:**

- REST API endpoint: `GET /api/stats`
- Формат данных: JSON с метриками + временной ряд для графика
- Темная тема (shadcn/ui стиль)
- MVP: без авторизации, локальный запуск, in-memory данные

**Формат API ответа:**

```json
{
  "overview": {
    "total_users": {"value": 150, "trend": 12.5, "trend_direction": "up"},
    "total_conversations": {...},
    "total_messages": {...},
    "avg_conversation_length": {...}
  },
  "message_activity": {
    "data_points": [
      {"timestamp": "2025-10-15T00:00:00Z", "message_count": 45}
    ]
  }
}
```

## Критерии готовности

- Документ создан, краткий и понятный
- Описаны UI компоненты и API структура
- Определен визуальный стиль (shadcn/ui)

### To-dos

- [ ] Изучить текущую структуру ContextManager и Message для понимания доступных данных
- [ ] Создать doc/dashboard-requirements.md с детальным описанием UI компонентов, темной темы и графиков
- [ ] Создать doc/api-design.md со спецификацией REST API endpoint /api/stats включая структуру данных для графиков
- [ ] Документировать необходимые изменения в архитектуре (добавление timestamp к Message)