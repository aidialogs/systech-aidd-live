# Инструкция по тестированию Docker Setup

Этот документ содержит пошаговую инструкцию для проверки работоспособности Docker окружения.

## Предварительная подготовка

### 1. Проверка наличия Docker

```bash
docker --version
# Ожидается: Docker version 20.10+ или выше

docker compose version
# Ожидается: Docker Compose version v2.0+ или выше
```

### 2. Создание файла .env

```bash
# Из корня проекта
cp devops/env.example .env
```

Отредактируйте `.env` и заполните следующие обязательные переменные:

- `BOT_TOKEN` - получите от @BotFather в Telegram
- `LLM_API_KEY` - API ключ от OpenRouter или другого провайдера
- `LLM_BASE_URL` - URL API (например, https://openrouter.ai/api/v1)
- `LLM_MODEL` - модель LLM (например, anthropic/claude-3.5-sonnet)

Остальные переменные можно оставить по умолчанию.

## Тестирование

### Шаг 1: Сборка образов

```bash
cd devops
docker compose build
```

**Ожидаемый результат:**
- Успешная сборка 3 образов: bot, api, frontend
- Время сборки: 3-10 минут при первом запуске
- Вывод должен завершиться без ошибок

**Проверка:**
```bash
docker images | grep systech-aidd
```

Должны быть видны 3 образа:
- devops-bot
- devops-api  
- devops-frontend

### Шаг 2: Запуск всех сервисов

```bash
docker compose up
```

**Ожидаемый результат:**

1. **PostgreSQL запускается первым:**
```
systech-aidd-postgres | database system is ready to accept connections
```

2. **Bot запускается после PostgreSQL:**
```
systech-aidd-bot | Running migrations...
systech-aidd-bot | INFO: Applying migration: 09eb92e9cbfc - create users and messages tables
systech-aidd-bot | Database initialized
systech-aidd-bot | Bot started
```

3. **API запускается после PostgreSQL:**
```
systech-aidd-api | INFO: Started server process
systech-aidd-api | INFO: Uvicorn running on http://0.0.0.0:8000
```

4. **Frontend запускается после API:**
```
systech-aidd-frontend | ready - started server on 0.0.0.0:3000
```

### Шаг 3: Проверка доступности сервисов

Откройте новый терминал и выполните проверки:

#### 3.1 Проверка API

```bash
curl http://localhost:8000/health
# Ожидается: {"status":"ok"}

curl http://localhost:8000/
# Ожидается: JSON с информацией об API
```

Откройте в браузере:
- http://localhost:8000/docs - должна открыться Swagger документация

#### 3.2 Проверка Frontend

Откройте в браузере:
- http://localhost:3000 - должна открыться главная страница
- http://localhost:3000/dashboard - должна открыться дашборд страница

#### 3.3 Проверка Bot

1. Откройте Telegram
2. Найдите вашего бота по токену
3. Отправьте команду `/start`
4. **Ожидается:** Бот должен ответить приветственным сообщением

В логах должно появиться:
```
systech-aidd-bot | INFO: Received message from user 12345678
systech-aidd-bot | INFO: Handled /start command
```

#### 3.4 Проверка взаимодействия Frontend-API

1. Откройте http://localhost:3000/dashboard
2. Проверьте, что отображается статистика (графики)
3. Перейдите на страницу чата
4. Отправьте сообщение в чат
5. **Ожидается:** Бот должен ответить

### Шаг 4: Проверка базы данных

```bash
# Подключение к PostgreSQL
docker compose exec postgres psql -U systech_user -d systech_aidd

# В psql выполните:
\dt  # Список таблиц - должны быть users и messages

SELECT COUNT(*) FROM users;
# После теста с ботом должна быть хотя бы одна запись

SELECT COUNT(*) FROM messages;
# После теста с ботом должно быть несколько записей

\q  # Выход из psql
```

### Шаг 5: Проверка логов

```bash
# Просмотр логов всех сервисов
docker compose logs

# Логи конкретного сервиса
docker compose logs bot
docker compose logs api
docker compose logs postgres
docker compose logs frontend
```

### Шаг 6: Остановка сервисов

```bash
# Нажмите Ctrl+C в терминале, где запущен docker compose up

# Или в другом терминале:
docker compose down
```

**Ожидаемый результат:**
- Все контейнеры останавливаются корректно
- Данные в PostgreSQL сохраняются (volume не удаляется)

### Шаг 7: Повторный запуск

```bash
docker compose up
```

**Проверка:**
- Сервисы запускаются быстрее (кэш)
- Данные в БД сохранились (пользователи и сообщения)
- Миграции не применяются повторно (уже применены)

## Тесты на устойчивость

### Тест 1: Перезапуск отдельного сервиса

```bash
docker compose restart bot
# Бот должен остановиться и запуститься заново

docker compose restart api
# API должен перезапуститься
```

### Тест 2: Очистка всех данных

```bash
docker compose down -v
# Удаляет контейнеры и volumes (включая данные БД)

docker compose up
# Запускается с чистой БД, миграции применяются заново
```

### Тест 3: Сборка с нуля

```bash
docker compose down
docker compose build --no-cache
docker compose up
```

## Чек-лист успешного тестирования

- [ ] Docker установлен и работает
- [ ] Файл .env создан и заполнен
- [ ] Сборка образов прошла успешно
- [ ] PostgreSQL запустился и прошел healthcheck
- [ ] Bot запустился и применил миграции
- [ ] API запустился на порту 8000
- [ ] Frontend запустился на порту 3000
- [ ] API отвечает на /health endpoint
- [ ] Swagger docs доступны по /docs
- [ ] Frontend открывается в браузере
- [ ] Bot отвечает в Telegram на /start
- [ ] База данных содержит таблицы users и messages
- [ ] Логи всех сервисов без критических ошибок
- [ ] Сервисы корректно останавливаются
- [ ] Повторный запуск работает

## Известные проблемы и решения

### Проблема: Port already in use

**Решение:**
```bash
# Найдите процесс, занимающий порт
lsof -i :5432
lsof -i :8000
lsof -i :3000

# Остановите процесс или измените порт в docker-compose.yml
```

### Проблема: Bot не запускается - Missing BOT_TOKEN

**Решение:**
- Проверьте, что .env файл находится в корне проекта
- Убедитесь, что BOT_TOKEN заполнен
- Перезапустите: `docker compose restart bot`

### Проблема: Медленная сборка

**Решение:**
- Это нормально при первой сборке
- Используйте BuildKit: `export DOCKER_BUILDKIT=1`
- Последующие сборки будут быстрее

### Проблема: Frontend не может подключиться к API

**Решение:**
- Проверьте, что API запущен: `curl http://localhost:8000/health`
- Проверьте NEXT_PUBLIC_API_URL в docker-compose.yml
- Проверьте CORS настройки в src/api/main.py

## Результаты тестирования

После успешного прохождения всех тестов заполните:

**Дата тестирования:** _____________

**Версии:**
- Docker: _____________
- Docker Compose: _____________

**Результаты:**
- [ ] Все тесты пройдены успешно
- [ ] Есть проблемы (описать ниже)

**Проблемы и замечания:**
_________________________________________
_________________________________________
_________________________________________

**Тестировал:** _____________

**Статус:** ✅ PASSED / ❌ FAILED

