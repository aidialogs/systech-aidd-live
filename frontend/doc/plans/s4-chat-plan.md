# Sprint S4: Реализация ИИ-чата - План реализации

## Статус: ✅ Completed

## Обзор

Создан полнофункциональный веб-чат с поддержкой двух режимов работы:
- **Обычный режим**: общение с LLM-ассистентом (аналог бота)
- **Режим администратора**: аналитика данных с text2sql pipeline

Дашборд переведен с Mock API на реальную интеграцию с БД.

## Backend: Реализованные компоненты

### 1. RealStatCollector (`src/api/stat_collector_real.py`)

Реальный сборщик статистики с SQL запросами к PostgreSQL:
- Подсчет всех метрик из БД (messages, users, chats)
- Группировка по ролям и времени
- Фильтрация по периодам (day/week/month/all)
- Использование SQLAlchemy async queries

### 2. Chat Schemas (`src/api/chat_schemas.py`)

Pydantic модели:
- `ChatMessage` - одно сообщение чата
- `ChatRequest` - запрос с сообщением и режимом
- `ChatResponse` - ответ с сообщением и SQL (для debug)

### 3. ChatHandler (`src/api/chat_handler.py`)

Обработчик чат-запросов с двумя режимами:

**Normal Mode:**
- Использует ContextManager для управления контекстом
- Сохраняет все сообщения в БД
- Аналог MessageHandler из бота

**Admin Mode (Text2SQL pipeline):**
1. Генерация SQL запроса из вопроса пользователя
2. Валидация SQL (только SELECT)
3. Выполнение запроса
4. Формирование естественного ответа через LLM
5. Возврат ответа + SQL для отладки

### 4. API Endpoints (`src/api/main.py`)

Новые endpoints:
- `POST /api/v1/chat/message` - отправка сообщения
- `GET /api/v1/chat/history` - получение истории

### 5. API Server Integration (`src/api_server.py`)

- Инициализация RealStatCollector при mode="real"
- Инициализация LLMClient и ChatHandler
- Передача обоих в create_app()

## Frontend: Реализованные компоненты

### UI Components

Базовые компоненты из референса:
1. `ui/avatar.tsx` - аватары
2. `ui/textarea.tsx` - текстовая область
3. `ui/badge.tsx` - бейджи
4. `ui/message-loading.tsx` - индикатор загрузки
5. `ui/chat-bubble.tsx` - пузыри сообщений
6. `ui/chat-input.tsx` - поле ввода
7. `ui/chat-message-list.tsx` - список сообщений с auto-scroll
8. `ui/expandable-chat.tsx` - раскрывающийся чат
9. `hooks/use-auto-scroll.ts` - автопрокрутка

### Chat Components

1. **ModeToggle** (`chat/mode-toggle.tsx`)
   - Переключатель Normal/Admin режимов
   - Badge для индикации Admin режима

2. **ChatInterface** (`chat/chat-interface.tsx`)
   - Основной компонент чата
   - Управление состоянием сообщений
   - Загрузка истории при монтировании
   - Отправка сообщений в API
   - Отображение SQL запросов в admin режиме

3. **FloatingChatButton** (`chat/floating-chat-button.tsx`)
   - Floating кнопка для dashboard и главной страницы
   - Раскрывающийся чат
   - Интеграция ModeToggle и ChatInterface

### API Client & Types

Обновления в `lib/api.ts`:
- `sendChatMessage()` - отправка сообщения
- `getChatHistory()` - получение истории

Обновления в `lib/types.ts`:
- `ChatMessage` - тип сообщения
- `ChatResponse` - тип ответа

### Pages

1. **Chat Page** (`app/chat/page.tsx`)
   - Полноэкранная страница чата
   - Переключатель режимов в header
   - Полнофункциональный чат интерфейс

2. **Dashboard Page** (обновлен)
   - Добавлен FloatingChatButton

3. **Home Page** (обновлен)
   - Добавлен FloatingChatButton

## Configuration & Testing

### Environment Variables

`.env` переменная для выбора режима:
```
STAT_COLLECTOR_MODE=real  # mock или real
```

### Makefile Commands

Новые команды для тестирования:
```bash
make chat-test          # Тест normal режима
make chat-test-admin    # Тест admin режима с text2sql
make chat-history       # Получение истории
```

## Функциональность

### Обычный режим
✅ Отправка сообщений к LLM
✅ Получение ответов
✅ История диалога из БД
✅ Контекст сохраняется автоматически
✅ Floating button на всех страницах

### Режим администратора
✅ Вопросы по статистике на естественном языке
✅ Text2SQL pipeline (вопрос → SQL → выполнение → ответ)
✅ Валидация SQL (только SELECT)
✅ Отображение SQL запросов для отладки
✅ Доступ к реальным данным из БД

### UI/UX
✅ Floating button в правом нижнем углу
✅ Раскрывающийся чат при нажатии
✅ Адаптивный дизайн (mobile/desktop)
✅ Индикатор режима (Normal/Admin)
✅ Toggle для переключения режимов
✅ Auto-scroll с кнопкой "вниз"
✅ Loading индикатор
✅ Полноэкранная страница /chat

### Dashboard Integration
✅ Real StatCollector вместо Mock
✅ SQL запросы к реальной БД
✅ Все метрики работают с данными из БД

## Технические детали

### Text2SQL Промпт

```
У тебя есть доступ к БД PostgreSQL с таблицами:

Таблица users:
- id (bigint, primary key) - ID пользователя Telegram
- created_at (timestamp) - дата создания
- is_deleted (boolean) - флаг удаления

Таблица messages:
- id (integer, primary key) - ID сообщения
- user_id (bigint, foreign key) - ID пользователя
- chat_id (bigint) - ID чата Telegram
- role (varchar) - роль: 'user', 'assistant', 'system'
- content (text) - текст сообщения
- content_length (integer) - длина сообщения
- created_at (timestamp) - дата создания
- is_deleted (boolean) - флаг удаления

Вопрос: "{user_question}"

Верни только SQL запрос (SELECT).
```

### SQL Safety

Реализована валидация:
- Запрос должен начинаться с SELECT
- Запрещены: INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, TRUNCATE, EXEC

### Dependencies

Добавленные NPM пакеты:
- `@radix-ui/react-avatar`

Остальные уже были в проекте:
- `lucide-react`
- `@radix-ui/react-slot`
- `class-variance-authority`

## Результаты

### Backend
- ✅ RealStatCollector с SQL запросами
- ✅ ChatHandler с normal и admin режимами
- ✅ Text2SQL pipeline полностью работает
- ✅ Chat API endpoints
- ✅ Интеграция с существующей БД

### Frontend
- ✅ 9 UI компонентов для чата
- ✅ ChatInterface с полным функционалом
- ✅ FloatingChatButton на всех страницах
- ✅ Полноэкранная страница /chat
- ✅ ModeToggle для переключения режимов
- ✅ Отображение SQL в admin режиме

### Testing
- ✅ Makefile команды для тестирования
- ✅ Работает с реальной БД
- ✅ Все endpoints функциональны

## Как использовать

1. Запустить API: `make api-run`
2. Запустить frontend: `make frontend-dev`
3. Открыть http://localhost:3000
4. Floating button доступен на главной странице и dashboard
5. Полноэкранный чат: http://localhost:3000/chat
6. Переключение режимов: Normal ↔ Admin

## Примеры использования

### Normal Mode
```
Пользователь: "Объясни что такое Python decorators?"
Ассистент: [Подробное объяснение от LLM]
```

### Admin Mode
```
Пользователь: "Сколько всего сообщений в базе данных?"
SQL: SELECT COUNT(*) FROM messages WHERE is_deleted = false
Ассистент: "В базе данных содержится 1234 сообщения."
```

## Следующие шаги

Sprint S4 завершен. Следующий Sprint S5 может включать:
- Дополнительные функции чата (voice input, file upload)
- Улучшение text2sql (более сложные запросы)
- Кэширование запросов
- Rate limiting
- Мониторинг и логирование



