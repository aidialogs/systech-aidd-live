# 🐳 Быстрый старт с Docker

Этот гайд поможет вам запустить весь проект локально через Docker одной командой.

## Требования

- **Docker** 20.10+ и **Docker Compose** 2.0+
- Около 2 GB свободного места на диске
- Доступ к интернету для скачивания образов

### Проверка установки Docker

```bash
docker --version
docker compose version
```

## Быстрый запуск

### Шаг 1: Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```bash
# Скопируйте шаблон
cp devops/env.example .env

# Отредактируйте файл и заполните переменные
nano .env  # или используйте любой редактор
```

Обязательно заполните следующие переменные:

```env
# Получите токен от @BotFather в Telegram
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Получите API ключ от OpenRouter или другого провайдера
LLM_API_KEY=sk-or-v1-...

# Настройте LLM
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=anthropic/claude-3.5-sonnet

# Остальные переменные можно оставить по умолчанию
DATABASE_URL=postgresql+asyncpg://systech_user:systech_password@postgres:5432/systech_aidd
DATABASE_ECHO=False
MAX_CONTEXT_MESSAGES=20
SYSTEM_PROMPT_FILE=prompts/system_prompt.txt
```

### Шаг 2: Запуск всех сервисов

```bash
# Перейдите в директорию devops
cd devops

# Запустите все сервисы
docker compose up
```

При первом запуске:
- Docker скачает все необходимые образы (Python, Node, PostgreSQL)
- Соберет образы для bot, api и frontend
- Это займет 5-10 минут в зависимости от скорости интернета

При последующих запусках все будет намного быстрее благодаря кэшу.

### Шаг 3: Проверка работоспособности

После запуска вы увидите логи всех сервисов. Проверьте:

✅ **PostgreSQL** запустился:
```
systech-aidd-postgres | database system is ready to accept connections
```

✅ **Bot** подключился к БД:
```
systech-aidd-bot | Database initialized
systech-aidd-bot | Bot started
```

✅ **API** запустился:
```
systech-aidd-api | Uvicorn running on http://0.0.0.0:8000
```

✅ **Frontend** запустился:
```
systech-aidd-frontend | ready - started server on 0.0.0.0:3000
```

### Шаг 4: Проверка доступности сервисов

Откройте в браузере:

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

Проверьте бота в Telegram - отправьте ему сообщение `/start`

## Управление сервисами

### Проверка статуса

```bash
# Красивый статус всех сервисов с проверкой доступности
make status
```

Эта команда покажет:
- 📊 Статус всех контейнеров
- 🏥 Health checks (PostgreSQL, Bot, API, Frontend)
- 🌐 Доступность сервисов (проверка портов и endpoints)
- 💾 Количество записей в базе данных
- 💻 Использование ресурсов (CPU и RAM)
- 📝 Полезные команды для управления

### Остановка

```bash
# Нажмите Ctrl+C в терминале, где запущены сервисы
# Или в другом терминале:
docker compose down
```

### Перезапуск после изменений в коде

```bash
# Пересоборка образов и запуск
docker compose up --build

# Или пересборка конкретного сервиса
docker compose build bot
docker compose up bot
```

### Запуск в фоновом режиме

```bash
# Запуск в detached mode
docker compose up -d

# Просмотр логов
docker compose logs -f

# Логи конкретного сервиса
docker compose logs -f bot
```

### Очистка данных

```bash
# Остановить и удалить все контейнеры и volumes
docker compose down -v

# Удалить неиспользуемые образы
docker image prune -a
```

## Структура сервисов

```
┌─────────────────────────────────────────────────┐
│                  Docker Network                  │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │   Bot    │  │   API    │  │ Frontend │      │
│  │  :---    │  │  :8000   │  │  :3000   │      │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘      │
│       │             │              │             │
│       └─────────────┴──────────────┘             │
│                     │                            │
│            ┌────────▼────────┐                   │
│            │   PostgreSQL    │                   │
│            │     :5432       │                   │
│            └─────────────────┘                   │
└─────────────────────────────────────────────────┘
```

## Часто встречающиеся проблемы

### Проблема: Порт уже занят

**Симптом:**
```
Error: bind: address already in use
```

**Решение:**
```bash
# Найдите процесс, занимающий порт
lsof -i :5432  # или :8000, :3000

# Остановите процесс или измените порт в docker-compose.yml
```

### Проблема: Миграции не применяются

**Симптом:**
```
sqlalchemy.exc.ProgrammingError: relation "users" does not exist
```

**Решение:**
```bash
# Проверьте логи бота - миграции должны применяться автоматически
docker compose logs bot

# Если миграции не применились, выполните вручную:
docker compose exec bot uv run alembic upgrade head
```

### Проблема: Bot не запускается из-за LLM_API_KEY

**Симптом:**
```
ConfigError: Missing required environment variables: LLM_API_KEY
```

**Решение:**
- Убедитесь, что файл `.env` создан в корне проекта (не в devops/)
- Проверьте, что все обязательные переменные заполнены
- Перезапустите сервисы: `docker compose restart bot`

### Проблема: Frontend не может подключиться к API

**Симптом:**
В консоли браузера: `Failed to fetch http://localhost:8000`

**Решение:**
- Убедитесь, что API запущен: `curl http://localhost:8000/health`
- Проверьте CORS настройки в `src/api/main.py`
- Очистите кэш браузера

### Проблема: Медленная сборка

**Симптом:**
Сборка образов занимает более 10 минут

**Решение:**
- Это нормально при первой сборке
- Последующие сборки будут использовать кэш слоев Docker
- Для ускорения можно настроить BuildKit:
  ```bash
  export DOCKER_BUILDKIT=1
  ```

## Полезные команды

```bash
# Красивый статус всех сервисов (рекомендуется!)
make status

# Статус всех контейнеров
docker compose ps

# Логи всех сервисов
docker compose logs

# Логи конкретного сервиса с автообновлением
docker compose logs -f bot

# Выполнить команду в контейнере
docker compose exec bot uv run python -c "print('Hello')"

# Подключиться к PostgreSQL
docker compose exec postgres psql -U systech_user -d systech_aidd

# Посмотреть использование ресурсов
docker stats

# Перезапустить конкретный сервис
docker compose restart api

# Остановить конкретный сервис
docker compose stop frontend
```

## Разработка с Docker

### Горячая перезагрузка (hot reload)

Для разработки можно монтировать локальные файлы в контейнеры.

Добавьте в `docker-compose.yml`:

```yaml
# Для bot/api сервисов
volumes:
  - ../src:/app/src:ro  # read-only монтирование

# Для frontend
volumes:
  - ../frontend:/app
  - /app/node_modules  # exclude node_modules
```

**Внимание:** Python сервисы нужно будет перезапускать вручную после изменений.

### Отладка

Для подключения отладчика измените CMD в Dockerfile:

```dockerfile
# Для Python сервисов
CMD ["uv", "run", "python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "src.main"]
```

И добавьте порт в docker-compose.yml:
```yaml
ports:
  - "5678:5678"  # debugpy port
```

## Что дальше?

После успешного запуска через Docker:

1. 📖 Изучите [Архитектуру проекта](../../doc/guides/02-architecture.md)
2. 🧪 Запустите тесты: `docker compose exec bot uv run pytest`
3. 🚀 Переходите к следующему спринту - Production Ready Docker Setup

## Дополнительная информация

- 📚 **Docker документация**: https://docs.docker.com/
- 🐳 **Docker Compose**: https://docs.docker.com/compose/
- 📝 **DevOps Roadmap**: [devops-roadmap.md](../devops-roadmap.md)
- 🏠 **Основная документация**: [README.md](../../README.md)

---

**Готово! Весь проект запущен в Docker! 🎉**

