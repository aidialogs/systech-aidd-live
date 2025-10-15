# План разработки UI Dashboard

> Базовый проект реализован: @tasklist.md  
> Техническое видение: @vision.md  
> Правила разработки: @conventions.mdc

---

## 📊 Прогресс разработки

| Итерация | Задача | Статус | Дата | План |
|----------|--------|--------|------|------|
| 1️⃣ | Анализ требований и проектирование API | ✅ Завершено | 2025-10-15 | [План](.cursor/plans/frontend-1.plan.md) |
| 2️⃣ | Реализация Stats API (заглушка) | ✅ Завершено | 2025-10-15 | [План](.cursor/plans/dashboard-api-implementation-1c94bc81.plan.md) |
| 3️⃣ | Концепция Frontend (front-vision.md) | ⏳ Ожидает | - | - |
| 4️⃣ | Выбор стека и инициализация проекта | ⏳ Ожидает | - | - |
| 5️⃣ | Базовая структура UI | ⏳ Ожидает | - | - |
| 6️⃣ | Реализация Dashboard страницы | ⏳ Ожидает | - | - |
| 7️⃣ | Интеграция с API | ⏳ Ожидает | - | - |
| 8️⃣ | Финальное тестирование | ⏳ Ожидает | - | - |

**Легенда статусов:**
- ⏳ Ожидает
- 🚧 В работе
- ✅ Завершено
- ⚠️ Требует доработки

---

## 🚀 Итерации разработки

### Итерация 1: Анализ требований и проектирование API

**Цель:** Определить минимальный набор метрик для дашборда и спроектировать единый API endpoint

**Принцип:** KISS - используем только существующие данные из ContextManager, без усложнений

**Анализ данных:**
- [x] Изучить структуру ContextManager (in-memory хранилище)
- [x] Определить доступные метрики из существующих данных
- [x] Учесть ограничение: данные теряются при перезапуске

**Документы для создания:**
- [ ] `doc/dashboard-requirements.md` - функциональные требования к дашборду
  - **Общая статистика** (Overview):
    - Общее количество уникальных пользователей
    - Общее количество активных диалогов
    - Общее количество сообщений (user + assistant)
    - Средняя длина диалога (сообщений на диалог)
  - **Топ активных пользователей** (Top Users):
    - User ID
    - Количество сообщений
    - Дата последней активности
  - **Последние диалоги** (Recent Conversations):
    - User ID / Chat ID
    - Количество сообщений в диалоге
    - Последнее сообщение (превью)
    - Timestamp последнего сообщения

- [ ] `doc/api-design.md` - спецификация REST API
  - **Единственный endpoint**: `GET /api/stats`
  - **Формат ответа** (JSON):
    ```json
    {
      "overview": {
        "total_users": 0,
        "total_conversations": 0,
        "total_messages": 0,
        "avg_conversation_length": 0.0
      },
      "top_users": [
        {
          "user_id": 0,
          "username": "string",
          "message_count": 0,
          "last_activity": "ISO8601"
        }
      ],
      "recent_conversations": [
        {
          "user_id": 0,
          "chat_id": 0,
          "message_count": 0,
          "last_message_preview": "string",
          "last_activity": "ISO8601"
        }
      ]
    }
    ```
  - **Технические детали**:
    - Метод: GET
    - Аутентификация: отсутствует (MVP)
    - CORS: разрешен для localhost
    - Формат даты: ISO 8601

**Ключевые решения:**
- Один универсальный endpoint вместо множества мелких
- Данные агрегируются из ContextManager при каждом запросе
- Без персистентного хранилища (in-memory only)
- Без сложной аналитики - только базовые метрики

**Тест:**
- Документы созданы и понятны
- API спецификация минимальна и достаточна
- Формат JSON ответа согласован

---

### Итерация 2: Реализация Stats API (заглушка)

**Цель:** Реализовать REST API endpoint с mock данными для разработки frontend

**Новые зависимости:**
- [ ] `pyproject.toml` - добавить:
  - `fastapi` - REST API framework
  - `uvicorn` - ASGI сервер

**Новые файлы:**
- [ ] `src/stats_collector.py` - класс StatsCollector
  - `__init__(context_manager: ContextManagerProtocol)` - DI через Protocol
  - `async def collect_stats() -> dict` - сбор всей статистики
  - **Пока возвращает mock данные** для красивого дашборда:
    ```python
    return {
        "overview": {
            "total_users": 15,
            "total_conversations": 23,
            "total_messages": 342,
            "avg_conversation_length": 14.9
        },
        "top_users": [...],  # 5-10 пользователей с разной активностью
        "recent_conversations": [...]  # 10 последних диалогов
    }
    ```

- [ ] `src/api_server.py` - FastAPI приложение
  - Определение FastAPI app
  - CORS middleware (allow localhost origins)
  - `GET /api/stats` endpoint:
    ```python
    @app.get("/api/stats")
    async def get_stats():
        stats = await stats_collector.collect_stats()
        return stats
    ```
  - Health check endpoint: `GET /health`

- [ ] `src/api_main.py` - точка входа для API сервера
  - Инициализация Config, ContextManager, StatsCollector
  - Запуск uvicorn с конфигурацией из .env

**Доработка конфигурации:**
- [ ] `src/config.py`:
  - Добавить поля: `api_host: str`, `api_port: int`
  - Defaults: `API_HOST=0.0.0.0`, `API_PORT=8000`
- [ ] `.env.example`:
  - Добавить `API_HOST=0.0.0.0`
  - Добавить `API_PORT=8000`

**Доработка Makefile:**
- [ ] Добавить команду `run-api`:
  ```makefile
  run-api:
      uv run python -m src.api_main
  ```

**Логирование:**
- [ ] Логировать запуск API сервера (host, port)
- [ ] Логировать каждый API запрос (endpoint, response time)
- [ ] Использовать существующую систему логирования из main.py

**Архитектура:**
```
┌─────────────────┐
│  Telegram Bot   │
│  (src/main.py)  │
└────────┬────────┘
         ↓
  ContextManager
  (in-memory)
         ↑
┌────────┴────────┐
│   API Server    │
│ (src/api_main)  │
│        ↓        │
│ StatsCollector  │
│   (mock data)   │
└─────────────────┘
```

**Функционал:**
- FastAPI сервер работает независимо от бота
- Endpoint `/api/stats` возвращает mock данные
- CORS настроен для локальной разработки
- Health check для проверки доступности

**Тесты:**
- [ ] `tests/test_stats_collector.py`:
  - Тест создания StatsCollector
  - Тест возврата mock данных (структура корректна)
- [ ] `tests/test_api_server.py`:
  - Тест GET /api/stats (status 200, корректный JSON)
  - Тест GET /health (status 200)
  - Тест CORS headers

**Тест (мануальный):**
1. Запустить API: `make run-api`
2. Проверить `curl http://localhost:8000/health` → `{"status": "ok"}`
3. Проверить `curl http://localhost:8000/api/stats` → JSON с mock данными
4. Открыть `http://localhost:8000/docs` → увидеть Swagger UI
5. Проверить логи → есть запись о запуске API сервера
6. Запустить тесты: `make test` → все проходят

---

### Итерация 3: Концепция Frontend (front-vision.md)

**Цель:** Определить техническое видение frontend приложения

**Документ для создания:**
- [ ] `dashboard/doc/front-vision.md` - техническое видение frontend

**Содержание документа:**

1. **Описание проекта**
   - Название: Dashboard для статистики Telegram бота
   - Назначение: визуализация метрик диалогов в реальном времени
   - Целевая аудитория: разработчики/администраторы бота

2. **Технологический стек** (детали в Итерации 4)
   - Framework: Next.js
   - UI Components: shadcn/ui
   - Package Manager: pnpm
   - Styling: Tailwind CSS
   - TypeScript: strict mode

3. **Структура приложения**
   - Single Page Application (SPA)
   - Одна главная страница - Dashboard
   - Без роутинга (пока не нужно)
   - Responsive design (desktop first)

4. **Основные секции Dashboard**
   - **Overview Cards** (4 карточки):
     - Total Users
     - Total Conversations
     - Total Messages
     - Avg Conversation Length
   - **Top Users Table**:
     - Колонки: User ID, Username, Messages, Last Activity
     - Сортировка по количеству сообщений
     - Топ 10 пользователей
   - **Recent Conversations Table**:
     - Колонки: User/Chat ID, Messages, Last Message, Time
     - 10 последних диалогов
     - Превью последнего сообщения

5. **UI/UX Принципы**
   - Минимализм (KISS)
   - Светлая тема (можно темную позже)
   - Чистый и современный дизайн
   - Быстрая загрузка (<2 сек)

6. **Технические требования**
   - TypeScript strict mode (type safety)
   - Responsive design (desktop/tablet/mobile)
   - Auto-refresh каждые 30 сек (опционально)
   - Обработка ошибок API

7. **Ограничения MVP**
   - Только чтение данных (no CRUD)
   - Без аутентификации
   - Локальный запуск (без деплоя)
   - Без продвинутой аналитики
   - Без фильтрации/поиска

8. **Что НЕ делаем**
   - ❌ Редактирование данных
   - ❌ Авторизация пользователей
   - ❌ Real-time updates (WebSocket)
   - ❌ Экспорт данных
   - ❌ Множественные страницы
   - ❌ Сложные графики и визуализации

**Тест:**
- Документ создан и согласован
- Видение понятно и минимально
- Соответствует принципу KISS

---

### Итерация 4: Выбор стека и инициализация проекта

**Цель:** Инициализировать Next.js проект с необходимыми инструментами

**Технологический стек:**
- **Framework**: Next.js 14+ (App Router)
- **Package Manager**: pnpm
- **UI Components**: shadcn/ui
- **Styling**: Tailwind CSS
- **Language**: TypeScript (strict mode)
- **HTTP Client**: native fetch (Next.js)
- **UI Icons**: lucide-react (из shadcn/ui)

**Инициализация проекта:**
- [ ] Создать директорию `dashboard/`
- [ ] Выполнить `pnpm create next-app@latest . --typescript --tailwind --app --no-src-dir`
- [ ] Настроить shadcn/ui: `pnpm dlx shadcn@latest init`
- [ ] Установить компоненты shadcn/ui:
  - `pnpm dlx shadcn@latest add card`
  - `pnpm dlx shadcn@latest add table`
  - `pnpm dlx shadcn@latest add badge`

**Структура проекта:**
```
dashboard/
├── doc/
│   └── front-vision.md
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Dashboard page
│   └── globals.css         # Global styles
├── components/
│   ├── ui/                 # shadcn/ui components
│   ├── overview-cards.tsx  # Metrics cards
│   ├── top-users-table.tsx # Top users table
│   └── recent-conversations-table.tsx
├── lib/
│   ├── utils.ts            # Utility functions
│   └── api.ts              # API client
├── types/
│   └── stats.ts            # TypeScript types for API
├── .env.example
├── .env.local
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── README.md
```

**Конфигурация:**
- [ ] `.env.example`:
  ```
  NEXT_PUBLIC_API_URL=http://localhost:8000
  ```
- [ ] `tsconfig.json` - strict mode:
  ```json
  {
    "compilerOptions": {
      "strict": true,
      "noUncheckedIndexedAccess": true
    }
  }
  ```

**Базовые файлы:**
- [ ] `dashboard/types/stats.ts` - TypeScript интерфейсы для API
- [ ] `dashboard/lib/api.ts` - API клиент (заглушка)
- [ ] `dashboard/README.md` - инструкция по запуску

**Тест:**
1. Установить зависимости: `pnpm install`
2. Запустить dev сервер: `pnpm dev`
3. Открыть `http://localhost:3000` → увидеть стартовую страницу Next.js
4. Проверить что TypeScript работает (создать компонент с типами)
5. Проверить что Tailwind работает (добавить стили)
6. Проверить что shadcn/ui работает (импортировать Card)

---

### Итерация 5: Базовая структура UI

**Цель:** Создать layout и базовые компоненты для Dashboard

**Детали:** _Будут уточнены при реализации_

**Основные задачи:**
- [ ] Создать основной layout с header
- [ ] Реализовать базовые UI компоненты
- [ ] Настроить TypeScript типы для API
- [ ] Создать API клиент (пока с mock данными на фронте)

---

### Итерация 6: Реализация Dashboard страницы

**Цель:** Реализовать визуализацию всех секций Dashboard

**Детали:** _Будут уточнены при реализации_

**Основные задачи:**
- [ ] Компонент Overview Cards (4 метрики)
- [ ] Компонент Top Users Table
- [ ] Компонент Recent Conversations Table
- [ ] Responsive layout

---

### Итерация 7: Интеграция с API

**Цель:** Подключить frontend к реальному backend API

**Детали:** _Будут уточнены при реализации_

**Основные задачи:**
- [ ] Реализовать API клиент для `/api/stats`
- [ ] Подключить реальные данные к компонентам
- [ ] Обработка состояний: loading, error, success
- [ ] Auto-refresh (опционально)

---

### Итерация 8: Финальное тестирование

**Цель:** Проверить работу всей системы (Bot + API + Dashboard)

**Детали:** _Будут уточнены при реализации_

**Основные задачи:**
- [ ] Тестирование backend API
- [ ] Тестирование frontend dashboard
- [ ] Интеграционное тестирование
- [ ] Обновление документации
- [ ] Финальная проверка качества кода

---

## 📝 Принципы разработки Dashboard

### KISS (Keep It Simple, Stupid)
- Минимальный набор функций для MVP
- Один универсальный API endpoint
- Простой UI без излишеств

### Технологические решения
- ✅ Next.js - современный и производительный
- ✅ shadcn/ui - готовые качественные компоненты
- ✅ pnpm - быстрый package manager
- ✅ TypeScript strict - type safety

### Ограничения MVP
- ✅ In-memory данные (теряются при перезапуске бота)
- ✅ Локальный запуск (без деплоя)
- ✅ Без авторизации
- ✅ Только чтение (no CRUD)
- ✅ Одна страница (Dashboard only)

### Что НЕ делаем
- ❌ Персистентное хранилище (БД)
- ❌ Множественные страницы и роутинг
- ❌ Сложные графики и аналитика
- ❌ Real-time обновления (WebSocket)
- ❌ Авторизация/аутентификация
- ❌ Деплой на production

---

## 🎯 Критерии успеха MVP

- [ ] API endpoint `/api/stats` возвращает все необходимые данные
- [ ] Dashboard отображает метрики в красивом виде
- [ ] Система работает локально (bot + API + dashboard)
- [ ] Код качественный (TypeScript strict, lint, tests)
- [ ] Документация актуальна
- [ ] Следование принципу KISS

---

