# Frontend Development

Этот каталог содержит документацию и ресурсы для разработки пользовательского интерфейса (frontend) проекта systech-aidd-live.

## 📋 Документация

- **[Frontend Roadmap](doc/frontend-roadmap.md)** - дорожная карта развития frontend
- **[Dashboard Requirements](doc/dashboard-requirements.md)** - функциональные требования к дашборду
- **[Sprint F1 Summary](doc/sprint-f1-summary.md)** - результаты первого спринта

## 🚀 Mock API для разработки

Mock API предоставляет фиксированные данные для разработки frontend без необходимости реальной базы данных.

### Быстрый старт

```bash
# Установка зависимостей
make install

# Запуск API сервера
make api-run
```

API будет доступен на `http://localhost:8000`

### Документация API

После запуска сервера откройте в браузере:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Endpoints

```bash
# Получить статистику за 7 дней
curl http://localhost:8000/api/stats?period=7d

# Получить статистику за 30 дней
curl http://localhost:8000/api/stats?period=30d

# Health check
curl http://localhost:8000/health
```

### Быстрое тестирование

```bash
# Показать информацию об API
make api-docs

# Протестировать все endpoints
make api-test
```

## 📊 Структура данных API

### Метрики

API возвращает 4 основные метрики с трендами:

- **total_users** - общее количество пользователей
- **total_chats** - количество активных диалогов
- **total_messages** - общее количество сообщений
- **avg_message_length** - средняя длина сообщения

Каждая метрика содержит:
- `value` - текущее значение
- `trend` - процент изменения (может быть положительным или отрицательным)

### Timeline

Массив точек данных для графика количества сообщений по дням:
- `date` - дата в формате ISO (YYYY-MM-DD)
- `messages` - количество сообщений за этот день

### Пример ответа

```json
{
  "metrics": {
    "total_users": {"value": 1250, "trend": 12.5},
    "total_chats": {"value": 1089, "trend": 8.3},
    "total_messages": {"value": 45678, "trend": 15.7},
    "avg_message_length": {"value": 142, "trend": 3.2}
  },
  "timeline": [
    {"date": "2025-10-11", "messages": 6234},
    {"date": "2025-10-12", "messages": 6521}
  ]
}
```

## 🎯 Roadmap

| Спринт | Описание | Статус |
|--------|----------|--------|
| F1 | Требования к дашборду и Mock API | ✅ Завершен |
| F2 | Каркас frontend проекта | 📋 Планируется |
| F3 | Реализация dashboard | 📋 Планируется |
| F4 | Реализация ИИ-чата | 📋 Планируется |
| F5 | Переход на реальный API | 📋 Планируется |

Подробности см. в [Frontend Roadmap](doc/frontend-roadmap.md)

## 🛠 Технологии

### Backend (Mock API)
- **FastAPI** - современный веб-фреймворк для Python
- **Uvicorn** - ASGI сервер
- **Python 3.11+** - язык разработки

### Планируемый Frontend Stack
Выбор технологий будет выполнен в спринте F2

## 📚 Дополнительные ресурсы

- [Референс дашборда](https://ui.shadcn.com/blocks#dashboard-01) - UI референс для дашборда
- [Project Vision](../doc/vision.md) - общее техническое видение проекта
- [Backend Roadmap](../doc/roadmap.md) - дорожная карта backend разработки

## 🤝 Разработка

### Структура каталога

```
frontend/
├── doc/                           # Документация
│   ├── frontend-roadmap.md       # Roadmap frontend
│   ├── dashboard-requirements.md # Требования к дашборду
│   └── sprint-f1-summary.md      # Итоги спринта F1
└── README.md                     # Этот файл
```

### Следующие шаги

После завершения спринта F2 здесь появится:
- Структура frontend проекта
- Конфигурация инструментов разработки
- Команды для сборки и разработки frontend

