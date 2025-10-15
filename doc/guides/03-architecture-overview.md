# 🏗️ Architecture Overview

**Цель**: Понять как всё работает вместе  
**Для кого**: Перед началом разработки  
**Время**: 20-30 минут

---

## 🎯 High-Level Architecture

```mermaid
graph TB
    User[👤 User<br/>Telegram] -->|Message| TG[Telegram Bot API]
    TG -->|aiogram| Bot[🤖 Bot<br/>Dispatcher]
    Bot --> MH[MessageHandler<br/>📨 Координатор]
    
    MH -->|Команда?| CH[CommandHandler<br/>⚡ Команды]
    MH -->|Сообщение| CM[ContextManager<br/>💾 Контекст]
    MH -->|LLM запрос| LC[LLMClient<br/>🧠 AI]
    
    CH -->|/reset| CM
    CM -->|История| MH
    LC -->|Ответ| MH
    MH -->|Response| Bot
    Bot -->|Message| TG
    TG -->|Ответ| User
    
    LC -->|API Call| LLM[OpenRouter<br/>🌐 LLM API]
    
    style User fill:#3498DB,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Bot fill:#2C3E50,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style MH fill:#E74C3C,stroke:#ECF0F1,stroke-width:3px,color:#ECF0F1
    style CH fill:#27AE60,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style CM fill:#F39C12,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style LC fill:#9B59B6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style LLM fill:#34495E,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
```

---

## 📦 Компоненты системы

### 🤖 main.py - Entry Point
**Ответственность**: Инициализация и запуск
- Загрузка конфигурации из .env
- Создание всех компонентов
- Настройка logging
- Запуск polling

### 📨 MessageHandler - Координатор
**Ответственность**: Оркестрация обработки
- Делегирует команды в CommandHandler
- Управляет контекстом через ContextManager
- Вызывает LLM через LLMClient
- Обрабатывает ошибки

### ⚡ CommandHandler - Команды
**Ответственность**: Обработка команд бота
- `/start` - приветствие
- `/help` - справка
- `/reset` - очистка контекста
- `/role` - показать промпт

### 💾 ContextManager - Хранение
**Ответственность**: Управление историей
- In-memory хранилище: `dict[(user_id, chat_id), list[Message]]`
- Добавление сообщений
- Автообрезка при превышении лимита
- Очистка контекста

### 🧠 LLMClient - AI Integration
**Ответственность**: Работа с LLM API
- Отправка запросов к OpenRouter
- Конвертация Message → OpenAI format
- Обработка ошибок API

---

## 🔄 Flow обработки сообщения

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant T as Telegram API
    participant B as Bot/Dispatcher
    participant MH as MessageHandler
    participant CH as CommandHandler
    participant CM as ContextManager
    participant LC as LLMClient
    participant LLM as OpenRouter API

    U->>T: Отправить сообщение
    T->>B: Webhook/Polling
    B->>MH: handle_message(message, user_id, chat_id)
    
    alt Команда (starts with /)
        MH->>CH: handle_command(text, user_id, chat_id)
        alt /reset
            CH->>CM: clear_context(user_id, chat_id)
            CM-->>CH: ✓
        end
        CH-->>MH: Response text
    else Обычное сообщение
        MH->>CM: get_context(user_id, chat_id)
        CM-->>MH: list[Message] (история)
        
        MH->>CM: add_message(user_id, chat_id, user_message)
        CM-->>MH: ✓
        
        MH->>LC: get_response(messages)
        LC->>LLM: API Call (chat.completions.create)
        LLM-->>LC: AI Response
        LC-->>MH: response_text
        
        MH->>CM: add_message(user_id, chat_id, assistant_message)
        CM-->>MH: ✓
    end
    
    MH-->>B: response_text
    B->>T: Send message
    T->>U: Показать ответ

    style U fill:#3498DB,stroke:#ECF0F1,color:#ECF0F1
    style MH fill:#E74C3C,stroke:#ECF0F1,color:#ECF0F1
    style CH fill:#27AE60,stroke:#ECF0F1,color:#ECF0F1
    style CM fill:#F39C12,stroke:#ECF0F1,color:#ECF0F1
    style LC fill:#9B59B6,stroke:#ECF0F1,color:#ECF0F1
    style LLM fill:#34495E,stroke:#ECF0F1,color:#ECF0F1
```

---

## 🧩 Принципы дизайна

### SOLID

**S - Single Responsibility Principle**
- `CommandHandler` - только команды
- `ContextManager` - только контекст
- `LLMClient` - только LLM API

**O - Open/Closed** (не применяется жестко в MVP)

**L - Liskov Substitution** (не применяется, нет наследования)

**I - Interface Segregation**
- `LLMClientProtocol` - минимальный интерфейс для LLM
- `ContextManagerProtocol` - минимальный интерфейс для контекста

**D - Dependency Inversion**
- MessageHandler зависит от Protocol, не от конкретных классов
- Легкая подмена в тестах через моки

### KISS (Keep It Simple, Stupid)
- Плоская структура (нет глубокой вложенности)
- Один класс = один файл
- Минимум абстракций
- Никаких DI-контейнеров, фабрик, строителей

### DRY (Don't Repeat Yourself)
- `ContextManager._get_key()` - общий метод для создания ключа
- Фикстуры в `conftest.py` для переиспользования в тестах

---

## 🏛️ Архитектурные паттерны

### Coordinator Pattern
**MessageHandler** координирует взаимодействие компонентов.

**Плюсы**:
- Центральная точка контроля
- Легко отследить flow
- Простота понимания

### Strategy Pattern (через Protocols)
**Protocols** позволяют подменять реализации.

**Применение**:
- Тесты используют mock вместо реального LLMClient
- Можно подменить ContextManager на Redis-based

### In-Memory State
**ContextManager** хранит всё в памяти.

**Плюсы**: Простота, скорость  
**Минусы**: Потеря данных при рестарте

---

## 📊 Data Flow

```mermaid
graph LR
    A[User Message] --> B[MessageHandler]
    B --> C{Команда?}
    
    C -->|Да| D[CommandHandler]
    D --> E[Response]
    
    C -->|Нет| F[get_context]
    F --> G[ContextManager]
    G --> H[История<br/>list Messages]
    H --> I[add_user_message]
    I --> G
    
    G --> J[LLMClient]
    J --> K[OpenRouter API]
    K --> L[AI Response]
    L --> J
    J --> M[add_assistant_message]
    M --> G
    G --> E
    
    E --> N[Telegram API]
    N --> O[User]
    
    style A fill:#3498DB,stroke:#ECF0F1,color:#ECF0F1
    style B fill:#E74C3C,stroke:#ECF0F1,color:#ECF0F1
    style D fill:#27AE60,stroke:#ECF0F1,color:#ECF0F1
    style G fill:#F39C12,stroke:#ECF0F1,color:#ECF0F1
    style J fill:#9B59B6,stroke:#ECF0F1,color:#ECF0F1
    style K fill:#34495E,stroke:#ECF0F1,color:#ECF0F1
    style O fill:#3498DB,stroke:#ECF0F1,color:#ECF0F1
```

---

## 🔐 Обработка ошибок

```mermaid
graph TB
    Start[Получено сообщение] --> Try{try/except}
    
    Try -->|Success| Normal[Обработка]
    Normal --> Response[Ответ пользователю]
    
    Try -->|LLMError| LLMErr[Логировать<br/>+ дружелюбное<br/>сообщение]
    Try -->|Exception| GenErr[Логировать<br/>+ общее<br/>сообщение об ошибке]
    
    LLMErr --> UserMsg[Отправить<br/>пользователю]
    GenErr --> UserMsg
    
    UserMsg --> End[Завершение]
    Response --> End
    
    style Start fill:#3498DB,stroke:#ECF0F1,color:#ECF0F1
    style Normal fill:#27AE60,stroke:#ECF0F1,color:#ECF0F1
    style LLMErr fill:#E74C3C,stroke:#ECF0F1,color:#ECF0F1
    style GenErr fill:#E67E22,stroke:#ECF0F1,color:#ECF0F1
    style End fill:#95A5A6,stroke:#ECF0F1,color:#ECF0F1
```

**Стратегия**:
1. Все ошибки LLM API → `LLMError`
2. Все ошибки конфигурации → `ConfigError`
3. MessageHandler ловит все исключения
4. Пользователь всегда получает ответ (дружелюбное сообщение)
5. Все ошибки логируются с полным stack trace

---

## 📝 Логирование

**Что логируется**:

```python
# Lifecycle
"Bot started"
"Bot stopped"

# Сообщения
"Message from user_id=12345 chat_id=67890: 'Привет'"
"Command /start from user_id=12345"

# LLM
"LLM request: model=claude-3.5-sonnet, context_size=5"
"LLM response: duration=1.2s, status=success"

# Контекст
"Context created for user_id=12345 chat_id=67890"
"Context trimmed: 25 → 20 messages"

# Ошибки
"LLM API error: Connection timeout"
```

**Формат**: `YYYY-MM-DD HH:MM:SS | LEVEL | message`

**Выход**: `logs/app.log` + консоль

---

## ⚙️ Конфигурация

```mermaid
graph LR
    A[.env file] --> B[load_dotenv]
    B --> C[Config.from_env]
    C --> D{Валидация}
    
    D -->|OK| E[Config dataclass]
    D -->|Error| F[ConfigError<br/>+ список<br/>отсутствующих]
    
    E --> G[main]
    G --> H[Создание<br/>компонентов]
    
    F --> I[Выход<br/>с ошибкой]
    
    style A fill:#3498DB,stroke:#ECF0F1,color:#ECF0F1
    style C fill:#27AE60,stroke:#ECF0F1,color:#ECF0F1
    style E fill:#27AE60,stroke:#ECF0F1,color:#ECF0F1
    style F fill:#E74C3C,stroke:#ECF0F1,color:#ECF0F1
```

**Обязательные параметры**:
- `BOT_TOKEN`
- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL`

**Опциональные**:
- `SYSTEM_PROMPT_FILE` (default: `prompts/system_prompt.txt`)
- `MAX_CONTEXT_MESSAGES` (default: 20)

---

## 🧪 Тестируемость

**Dependency Injection через Protocols**:

```python
# В продакшене
llm_client = LLMClient(...)
context_manager = ContextManager(...)
message_handler = MessageHandler(llm_client, context_manager, ...)

# В тестах
mock_llm = AsyncMock(spec=LLMClientProtocol)
mock_llm.get_response.return_value = "Mocked response"
message_handler = MessageHandler(mock_llm, ...)
```

**Изоляция тестов**:
- LLM API не вызывается в unit тестах (моки)
- Integration тесты помечены маркером `@pytest.mark.integration`
- Фикстуры в `conftest.py` для переиспользования

---

## 🚀 Масштабируемость

### Текущие ограничения MVP:
- ❌ In-memory контекст (потеря при рестарте)
- ❌ Один процесс (нет горизонтального масштабирования)
- ❌ Polling (вместо webhook)
- ❌ Нет персистентного хранилища

### Пути масштабирования:
1. **Контекст** → Redis/PostgreSQL
2. **Polling** → Webhook + Load Balancer
3. **Горизонтальное масштабирование** → Несколько инстансов + общая БД
4. **Мониторинг** → Prometheus + Grafana
5. **Rate limiting** → Redis-based limiter

---

## 📚 Дополнительная информация

**ADR (Architecture Decision Records)**:
- [ADR-01](../adrs/ADR-01.md) - OpenAI Compatible API
- [ADR-02](../adrs/ADR-02.md) - Выбор OpenRouter
- [ADR-05](../adrs/ADR-05.md) - Архитектурный рефакторинг

**Следующие шаги**:
- [Data Model](04-data-model.md) - разобраться со структурами данных
- [Development Workflow](06-development-workflow.md) - начать разработку
- [Testing Strategy](07-testing-strategy.md) - как писать тесты

---

## 💡 Ключевые takeaways

1. **MessageHandler** - центральный координатор
2. **Protocols** обеспечивают DI и тестируемость
3. **Один класс = один файл** - легко найти код
4. **KISS** - нет избыточных абстракций
5. **Все ошибки логируются** - легко дебажить
6. **100% type hints** - безопасность типов
7. **In-memory state** - простота, но потеря данных при рестарте

