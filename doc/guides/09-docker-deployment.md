# GUIDE-09: Docker Deployment

Полное руководство по запуску systech-aidd-live через Docker контейнеры.

## Содержание

1. [Быстрый старт](#быстрый-старт)
2. [Требования](#требования)
3. [Структура Docker-инфраструктуры](#структура-docker-инфраструктуры)
4. [Production режим](#production-режим)
5. [Development режим](#development-режим)
6. [Управление контейнерами](#управление-контейнерами)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

---

## Быстрый старт

### Шаг 1: Подготовка окружения

```bash
# Клонировать репозиторий
git clone <repo-url>
cd systech-aidd-live

# Создать .env файл
cp .env.example .env
# Заполнить BOT_TOKEN, LLM_API_KEY и другие переменные
```

### Шаг 2: Запуск всех сервисов

```bash
# Сборка образов
make docker-build

# Запуск в detached режиме
make docker-up

# Проверка статуса
make docker-ps
```

### Шаг 3: Проверка работоспособности

```bash
# API Health check
curl http://localhost:8000/health
# Ожидаемый ответ: {"status":"ok"}

# Frontend
curl http://localhost:3000
# Должен вернуть HTML страницу

# Логи бота
docker compose -f devops/docker-compose.yml logs bot

# Проверка всех health checks
docker compose -f devops/docker-compose.yml ps
# Все сервисы должны быть (healthy)
```

---

## Требования

### Минимальные требования

- **Docker:** 20.10+ (с поддержкой BuildKit)
- **Docker Compose:** 2.0+ (v2 рекомендуется)
- **Свободное место:** ~2 GB для образов
- **RAM:** Минимум 4 GB (рекомендуется 8 GB)
- **Порты:** 3000, 5432, 8000 должны быть свободны

### Установка Docker

**macOS:**
```bash
brew install --cask docker
# Или скачайте Docker Desktop: https://www.docker.com/products/docker-desktop
```

**Linux (Ubuntu/Debian):**
```bash
# Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Docker Compose v2
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

**Проверка установки:**
```bash
docker --version          # Docker version 24.0+
docker compose version    # Docker Compose version 2.x
```

---

## Структура Docker-инфраструктуры

```
systech-aidd-live/
├── devops/
│   ├── Dockerfile.bot              # Multi-stage Dockerfile для Telegram бота
│   ├── Dockerfile.api              # Multi-stage Dockerfile для FastAPI
│   ├── Dockerfile.frontend         # Multi-stage Dockerfile для Next.js
│   ├── docker-compose.yml          # Production оркестрация
│   ├── docker-compose.dev.yml      # Development overrides
│   └── .hadolint.yaml              # Конфигурация линтера Dockerfile
├── .dockerignore                   # Исключения для Python сервисов
└── frontend/.dockerignore          # Исключения для Frontend

Сервисы:
├── postgres    (5432)  ← База данных PostgreSQL 16
├── bot                 ← Telegram бот (зависит от postgres)
├── api         (8000)  ← FastAPI сервер (зависит от postgres)
└── frontend    (3000)  ← Next.js UI (зависит от api)
```

### Описание образов

| Образ | Base Image | Размер | Особенности |
|-------|------------|--------|-------------|
| **systech-aidd-bot** | python:3.11-slim | ~180 MB | UV, alembic, non-root user |
| **systech-aidd-api** | python:3.11-slim | ~200 MB | FastAPI, uvicorn, health endpoint |
| **systech-aidd-frontend** | node:20-alpine | ~150 MB | Next.js standalone, optimized |

---

## Production режим

### Сборка образов

```bash
# Через Makefile (рекомендуется)
make docker-build

# Или напрямую через Docker Compose
docker compose -f devops/docker-compose.yml build

# Сборка конкретного сервиса
docker compose -f devops/docker-compose.yml build api

# Сборка без кэша (если нужна чистая пересборка)
docker compose -f devops/docker-compose.yml build --no-cache
```

### Запуск сервисов

```bash
# Запуск всех сервисов в detached режиме
make docker-up

# Или через Docker Compose
docker compose -f devops/docker-compose.yml up -d

# Запуск конкретного сервиса
docker compose -f devops/docker-compose.yml up -d api

# Запуск с просмотром логов (foreground)
docker compose -f devops/docker-compose.yml up
```

### Проверка статуса

```bash
# Статус всех контейнеров
docker compose -f devops/docker-compose.yml ps

# Подробная информация (с health checks)
docker compose -f devops/docker-compose.yml ps -a

# Только running контейнеры
docker ps --filter "name=systech-aidd"
```

### Просмотр логов

```bash
# Логи всех сервисов
make docker-logs

# Логи конкретного сервиса
docker compose -f devops/docker-compose.yml logs -f api

# Последние 100 строк
docker compose -f devops/docker-compose.yml logs --tail=100 bot

# Логи с timestamp
docker compose -f devops/docker-compose.yml logs -t frontend
```

### Остановка и удаление

```bash
# Остановка всех сервисов
make docker-down

# Или через Docker Compose
docker compose -f devops/docker-compose.yml down

# Остановка + удаление volumes (БД будет очищена!)
docker compose -f devops/docker-compose.yml down -v

# Остановка + удаление images
docker compose -f devops/docker-compose.yml down --rmi all
```

---

## Development режим

Development режим включает:
- 🔥 Hot reload для Python и Next.js
- 📁 Volume mounts для мгновенного отражения изменений
- 🐛 Debug порты (5678 для Python debugpy)
- 📊 Verbose логирование (DATABASE_ECHO=true)

### Запуск в dev режиме

```bash
# Через Makefile
make docker-dev

# Или через Docker Compose с двумя файлами
docker compose -f devops/docker-compose.yml -f devops/docker-compose.dev.yml up
```

### Что происходит в dev режиме

**API (FastAPI):**
- Uvicorn с `--reload` флагом
- Volume mount: `./src` → `/app/src` (read-only)
- Изменения в коде → автоматический перезапуск
- Debug port 5678 доступен для remote debugging

**Bot:**
- Volume mount: `./src` → `/app/src` (read-only)
- Изменения требуют ручного рестарта контейнера
- Verbose logging включен

**Frontend:**
- Next.js dev server (`pnpm dev`)
- Volume mount: `./frontend` → `/app` (cached)
- Hot Module Replacement (HMR) работает
- Изменения отражаются мгновенно

**PostgreSQL:**
- Порт 5432 expose для прямого доступа
- Можно подключаться через DBeaver/psql

### Подключение к БД в dev режиме

```bash
# Через docker exec
docker compose -f devops/docker-compose.yml exec postgres psql -U systech_user -d systech_aidd

# Через psql на хосте (если установлен)
psql postgresql://systech_user:systech_password@localhost:5432/systech_aidd

# Через DBeaver / TablePlus
Host: localhost
Port: 5432
Database: systech_aidd
User: systech_user
Password: systech_password
```

### Применение миграций

```bash
# Внутри контейнера API
docker compose -f devops/docker-compose.yml exec api alembic upgrade head

# Или через make (если настроено)
make db-migrate

# Создание новой миграции
docker compose -f devops/docker-compose.yml exec api alembic revision --autogenerate -m "описание"
```

### Remote debugging (Python)

```python
# Добавить в код (например, в src/api/main.py)
import debugpy
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()  # Опционально: ждать подключения отладчика

# В VSCode launch.json
{
  "name": "Docker API Debug",
  "type": "python",
  "request": "attach",
  "connect": {
    "host": "localhost",
    "port": 5678
  },
  "pathMappings": [
    {
      "localRoot": "${workspaceFolder}/src",
      "remoteRoot": "/app/src"
    }
  ]
}
```

---

## Управление контейнерами

### Выполнение команд внутри контейнера

```bash
# Запуск shell в контейнере
docker compose -f devops/docker-compose.yml exec api bash
docker compose -f devops/docker-compose.yml exec bot bash

# Выполнение Python команды
docker compose -f devops/docker-compose.yml exec api python -c "import src; print(src.__version__)"

# Запуск тестов внутри контейнера
docker compose -f devops/docker-compose.yml exec api pytest tests/

# Проверка переменных окружения
docker compose -f devops/docker-compose.yml exec api env | grep DATABASE
```

### Перезапуск сервисов

```bash
# Перезапуск всех сервисов
docker compose -f devops/docker-compose.yml restart

# Перезапуск конкретного сервиса
docker compose -f devops/docker-compose.yml restart api

# Перезапуск с новой сборкой (после изменения Dockerfile)
docker compose -f devops/docker-compose.yml up -d --build api
```

### Масштабирование

```bash
# Запуск нескольких инстансов API (для load testing)
docker compose -f devops/docker-compose.yml up -d --scale api=3

# Проверка
docker compose -f devops/docker-compose.yml ps api
```

### Инспекция контейнеров

```bash
# Детальная информация о контейнере
docker inspect systech-aidd-api

# Использование ресурсов (CPU, RAM)
docker stats systech-aidd-api

# Процессы внутри контейнера
docker compose -f devops/docker-compose.yml top api

# Размер контейнера и layers
docker compose -f devops/docker-compose.yml images
```

---

## Troubleshooting

### Проблема: Контейнер не запускается

**Симптомы:**
```
ERROR: Container exited with code 1
```

**Диагностика:**
```bash
# Смотрим логи
docker compose -f devops/docker-compose.yml logs bot

# Запускаем в foreground для просмотра ошибок
docker compose -f devops/docker-compose.yml up bot

# Проверяем переменные окружения
docker compose -f devops/docker-compose.yml config
```

**Частые причины:**
1. Отсутствует `.env` файл или не заполнены обязательные переменные
2. Порт уже занят другим процессом
3. Недостаточно памяти или места на диске
4. Ошибка в коде приложения

### Проблема: Health check fails

**Симптомы:**
```
api | unhealthy
```

**Диагностика:**
```bash
# Проверяем health check вручную
docker compose -f devops/docker-compose.yml exec api curl http://localhost:8000/health

# Если curl не установлен, используем wget или python
docker compose -f devops/docker-compose.yml exec api python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/health').read())"

# Смотрим логи запуска
docker compose -f devops/docker-compose.yml logs api | grep -i error
```

**Решение:**
- Увеличить `start_period` в healthcheck (особенно для медленных машин)
- Проверить, что приложение слушает на `0.0.0.0`, а не на `127.0.0.1`

### Проблема: Порт уже занят

**Симптомы:**
```
Error: bind: address already in use (port 8000)
```

**Решение:**
```bash
# Найти процесс на порту
lsof -i :8000        # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Убить процесс
kill -9 <PID>

# Или изменить порт в docker-compose.yml
ports:
  - "8001:8000"  # Внешний 8001, внутренний 8000
```

### Проблема: Медленная сборка

**Симптомы:**
- Сборка занимает > 10 минут
- Каждый раз пересобирается с нуля

**Решение:**
```bash
# Проверить, что BuildKit включен
export DOCKER_BUILDKIT=1

# Очистить старый build cache
docker builder prune

# Использовать cache-from (для CI)
docker compose -f devops/docker-compose.yml build --build-arg BUILDKIT_INLINE_CACHE=1

# Проверить .dockerignore
cat .dockerignore
cat frontend/.dockerignore
```

### Проблема: Volume permissions (Linux)

**Симптомы:**
```
Permission denied: '/app/logs/app.log'
```

**Решение:**
```bash
# Дать права на logs директорию
chmod -R 777 logs/

# Или создать с правильным владельцем
mkdir -p logs
chown -R 1001:1001 logs/

# В docker-compose.dev.yml использовать user mapping
user: "${UID}:${GID}"
```

### Проблема: Не работает hot reload в dev режиме

**Проверка:**
```bash
# Убедитесь, что используете dev compose файл
docker compose -f devops/docker-compose.yml -f devops/docker-compose.dev.yml ps

# Проверьте volume mounts
docker compose -f devops/docker-compose.yml -f devops/docker-compose.dev.yml config | grep volumes -A 5

# Проверьте логи uvicorn
docker compose -f devops/docker-compose.yml logs api | grep -i reload
```

### Проблема: Database connection refused

**Симптомы:**
```
asyncpg.exceptions.ConnectionRefusedError: Connection refused
```

**Диагностика:**
```bash
# Проверить статус postgres
docker compose -f devops/docker-compose.yml ps postgres

# Проверить health check
docker compose -f devops/docker-compose.yml exec postgres pg_isready -U systech_user

# Проверить depends_on в compose файле
docker compose -f devops/docker-compose.yml config | grep -A 5 depends_on
```

**Решение:**
- Убедиться, что используется service name (`postgres`) в DATABASE_URL, а не `localhost`
- Дождаться завершения health check postgres перед запуском зависимых сервисов

---

## Best Practices

### 1. Использование .env файла

```bash
# ✅ Хорошо: .env в корне проекта
BOT_TOKEN=your_token_here
LLM_API_KEY=your_api_key
DATABASE_URL=postgresql+asyncpg://systech_user:systech_password@postgres:5432/systech_aidd

# ❌ Плохо: Хардкод в docker-compose.yml
environment:
  BOT_TOKEN: "123456789:ABCDEF..."  # Никогда не коммитить в git!
```

### 2. Логирование

```bash
# Логи в файлы (через volume mount)
volumes:
  - ../logs:/app/logs

# Просмотр логов в real-time
docker compose -f devops/docker-compose.yml logs -f --tail=100

# Фильтрация по сервису
docker compose -f devops/docker-compose.yml logs api | grep ERROR
```

### 3. Очистка ресурсов

```bash
# Регулярная очистка (безопасно)
docker system prune

# Агрессивная очистка (удаляет volumes!)
docker system prune -a --volumes

# Очистка только build cache
docker builder prune

# Очистка неиспользуемых образов
docker image prune -a
```

### 4. Мониторинг ресурсов

```bash
# Использование CPU/RAM всех контейнеров
docker stats

# Размеры образов
docker images | grep systech-aidd

# Disk usage
docker system df
```

### 5. Backup базы данных

```bash
# Создать backup
docker compose -f devops/docker-compose.yml exec -T postgres pg_dump -U systech_user systech_aidd > backup_$(date +%Y%m%d).sql

# Восстановить из backup
cat backup_20251017.sql | docker compose -f devops/docker-compose.yml exec -T postgres psql -U systech_user systech_aidd

# Backup с volume
docker run --rm -v systech-aidd_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz /data
```

### 6. Security

```bash
# Сканирование уязвимостей (Trivy)
make docker-scan

# Или напрямую
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image systech-aidd-api:latest

# Проверка Dockerfile (Hadolint)
make docker-lint

# Или напрямую
docker run --rm -i hadolint/hadolint < devops/Dockerfile.api
```

### 7. Production deployment checklist

- [ ] Все secrets в environment variables (не в .env файле в repo)
- [ ] Health checks работают для всех сервисов
- [ ] Restart policies настроены (`restart: unless-stopped`)
- [ ] Логи собираются централизованно (ELK, Loki, CloudWatch)
- [ ] Мониторинг метрик (Prometheus, Grafana)
- [ ] Backup стратегия для БД
- [ ] Resource limits установлены в docker-compose.yml
- [ ] Security scanning в CI/CD pipeline
- [ ] Используется конкретная версия образов (не `latest`)

---

## Полезные команды

### Makefile shortcuts

```bash
make docker-build      # Сборка всех образов
make docker-up         # Запуск в production режиме
make docker-down       # Остановка всех сервисов
make docker-logs       # Просмотр логов
make docker-ps         # Статус контейнеров
make docker-clean      # Очистка (down + volumes + images)
make docker-dev        # Запуск в development режиме
make docker-lint       # Hadolint проверка Dockerfile
make docker-scan       # Trivy security scanning
```

### Docker Compose команды

```bash
# Общий формат
docker compose -f devops/docker-compose.yml [COMMAND]

# Основные команды
up -d              # Запуск в detached режиме
down               # Остановка и удаление контейнеров
ps                 # Статус контейнеров
logs -f [service]  # Логи (follow)
exec [service] sh  # Shell в контейнере
build [service]    # Сборка образа
restart [service]  # Перезапуск сервиса
pull               # Pull образов из registry
push               # Push образов в registry
```

---

## Дальнейшее чтение

- [ADR-08: Docker Best Practices](../adrs/ADR-08.md) - Архитектурные решения
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Hadolint](https://github.com/hadolint/hadolint) - Dockerfile linter
- [Trivy](https://aquasecurity.github.io/trivy/) - Security scanner

---

**Версия:** 1.0.0  
**Дата:** 2025-10-17  
**Автор:** DevOps Team

