# 🚀 Быстрая проверка Docker-инфраструктуры

Пошаговая инструкция для самостоятельной проверки Docker-образов и сервисов.

---

## Предварительные требования

```bash
# Проверьте, что Docker установлен и запущен
docker --version
# Ожидаемый результат: Docker version 20.10+ или выше

docker compose version
# Ожидаемый результат: Docker Compose version 2.x
```

---

## Шаг 1: Проверка файлов

```bash
# Перейдите в директорию проекта
cd /Users/akozhin/projects/systech-aidd-live

# Проверьте наличие всех Docker файлов
ls -la devops/Dockerfile.* devops/docker-compose.yml .dockerignore frontend/.dockerignore

# Ожидаемый результат: все файлы существуют
# - devops/Dockerfile.bot
# - devops/Dockerfile.api
# - devops/Dockerfile.frontend
# - devops/docker-compose.yml
# - devops/docker-compose.dev.yml
# - .dockerignore
# - frontend/.dockerignore
```

---

## Шаг 2: Hadolint - проверка Dockerfile

```bash
# Проверка качества Dockerfile
make docker-lint

# Ожидаемый результат: 
# - Несколько warnings (это нормально)
# - "Hadolint проверка завершена"
```

**Что проверяется:**
- Корректность синтаксиса Dockerfile
- Best practices для Docker
- Потенциальные проблемы безопасности

---

## Шаг 3: Сборка образов

```bash
# Собрать все Docker образы
make docker-build

# Ожидаемое время: ~1-2 минуты при первой сборке
# Ожидаемый результат: 
# [+] Building X.Xs (54/54) FINISHED
# ✔ devops-api       Built
# ✔ devops-bot       Built  
# ✔ devops-frontend  Built
```

**Что происходит:**
- Скачиваются базовые образы (python:3.11-slim, node:20-alpine)
- Устанавливаются зависимости через UV и pnpm
- Собираются multi-stage образы
- Оптимизируются слои для кэширования

**Возможные проблемы:**
- Если долго - это нормально при первой сборке (скачивание образов)
- Если ошибка с pnpm-lock.yaml - проверьте frontend/.dockerignore

---

## Шаг 4: Проверка размеров образов

```bash
# Посмотрите размеры собранных образов
docker images | grep devops

# Ожидаемый результат:
# devops-frontend   latest   ...   ~200-220 MB
# devops-api        latest   ...   ~300-330 MB
# devops-bot        latest   ...   ~300-320 MB
```

**Целевые размеры:**
- Frontend: ~150-220 MB ✅
- API: ~200-330 MB (приемлемо)
- Bot: ~180-320 MB (приемлемо)

---

## Шаг 5: Запуск сервисов

```bash
# Запустить все сервисы в фоновом режиме
make docker-up

# Ожидаемый результат:
# [+] Running 4/4
# ✔ Container systech-aidd-postgres  Healthy
# ✔ Container systech-aidd-bot       Started
# ✔ Container systech-aidd-api       Healthy
# ✔ Container systech-aidd-frontend  Started
```

**Что происходит:**
1. Создаётся сеть `systech-network`
2. Запускается PostgreSQL и ждёт healthy статуса
3. Запускаются Bot и API (ждут готовности БД)
4. Запускается Frontend (ждёт готовности API)

**Время запуска:** ~15-20 секунд

---

## Шаг 6: Проверка статуса контейнеров

```bash
# Проверить статус всех контейнеров
make docker-ps

# Альтернативно:
docker compose -f devops/docker-compose.yml ps

# Ожидаемый результат (через 30-60 секунд после запуска):
# NAME                   STATUS
# systech-aidd-postgres  Up (healthy) ✅
# systech-aidd-api       Up (healthy) ✅
# systech-aidd-bot       Up ✅
# systech-aidd-frontend  Up ✅
```

**Примечание:** Bot и Frontend могут показывать "unhealthy" - это известная проблема с health checks, но сервисы работают корректно.

---

## Шаг 7: Проверка логов

```bash
# Просмотр логов всех сервисов
make docker-logs

# Или логи конкретного сервиса:
docker compose -f devops/docker-compose.yml logs bot
docker compose -f devops/docker-compose.yml logs api
docker compose -f devops/docker-compose.yml logs frontend
docker compose -f devops/docker-compose.yml logs postgres
```

**Что проверять в логах:**

### Bot (должен содержать):
```
✅ Bot started
✅ System prompt loaded
✅ Database initialized
✅ Start polling
✅ Run polling for bot @airnd_bot
```

### API (должен содержать):
```
✅ Uvicorn running on http://0.0.0.0:8000
✅ Started server process [9]
✅ Started server process [10]
✅ Chat services initialized
✅ Application startup complete
```

### Frontend (должен содержать):
```
✅ Next.js 15.5.6
✅ Ready in XXms
```

### PostgreSQL (должен содержать):
```
✅ database system is ready to accept connections
```

**Если видите ошибки:** Прочитайте текст ошибки и проверьте .env файл.

---

## Шаг 8: Проверка HTTP доступности

### 8.1 API Health Check
```bash
curl http://localhost:8000/health

# Ожидаемый результат:
# {"status":"ok"}
```
✅ **PASS** если получили `{"status":"ok"}`  
❌ **FAIL** если "Connection refused" или другая ошибка

### 8.2 API Root Endpoint
```bash
curl http://localhost:8000/ | jq

# Ожидаемый результат:
# {
#   "message": "Systech AIDD Stats API",
#   "version": "1.0.0",
#   "docs": "/docs",
#   "stats_endpoint": "/api/stats"
# }
```

### 8.3 API Stats Endpoint
```bash
curl "http://localhost:8000/api/stats?period=7d" | jq .metrics

# Ожидаемый результат: JSON с метриками
# {
#   "total_users": {...},
#   "total_chats": {...},
#   ...
# }
```

### 8.4 Frontend
```bash
curl http://localhost:3000/ | head -20

# Ожидаемый результат: HTML страница с заголовком
# <!DOCTYPE html>...
# <title>Dashboard - Systech AIDD</title>
```

**Или откройте в браузере:**
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000
- API Stats: http://localhost:8000/api/stats?period=7d

---

## Шаг 9: Проверка межсервисного взаимодействия

```bash
# Проверить, что Bot подключён к БД
docker compose -f devops/docker-compose.yml logs bot | grep "Database initialized"

# Ожидаемый результат:
# ✅ Database initialized successfully

# Проверить, что API подключён к БД
docker compose -f devops/docker-compose.yml logs api | grep "Session factory created"

# Ожидаемый результат:
# ✅ Session factory created successfully
```

---

## Шаг 10: Остановка сервисов

```bash
# Остановить все сервисы
make docker-down

# Ожидаемый результат:
# [+] Running 5/5
# ✔ Container systech-aidd-frontend  Removed
# ✔ Container systech-aidd-bot       Removed
# ✔ Container systech-aidd-api       Removed
# ✔ Container systech-aidd-postgres  Removed
# ✔ Network devops_systech-network   Removed
```

**Примечание:** Данные PostgreSQL сохраняются в volume и не удаляются.

---

## Шаг 11 (Опционально): Полная очистка

```bash
# Удалить контейнеры, volumes и локальные образы
make docker-clean

# Ожидаемый результат:
# - Удалены все контейнеры
# - Удалены volumes (БД будет очищена!)
# - Удалены локальные образы
```

⚠️ **ВНИМАНИЕ:** Эта команда удалит все данные из PostgreSQL!

---

## 📋 Чек-лист быстрой проверки

Используйте этот чек-лист для проверки:

```bash
# 1. Проверка файлов
ls devops/Dockerfile.* devops/docker-compose.yml

# 2. Hadolint
make docker-lint

# 3. Сборка
make docker-build

# 4. Запуск
make docker-up

# 5. Подождать 30 секунд
sleep 30

# 6. Статус
make docker-ps

# 7. Проверка API
curl http://localhost:8000/health

# 8. Проверка Frontend
curl http://localhost:3000/ | head -5

# 9. Логи (если нужно)
make docker-logs | tail -50

# 10. Остановка
make docker-down
```

**Время выполнения:** ~3-5 минут

---

## 🐛 Troubleshooting

### Проблема: "Port already in use"
```bash
# Найти процесс на порту
lsof -i :8000
lsof -i :3000
lsof -i :5432

# Убить процесс
kill -9 <PID>

# Или остановить старые контейнеры
docker ps -a | grep systech-aidd
docker stop <container_name>
docker rm <container_name>
```

### Проблема: "Container name already in use"
```bash
# Удалить существующий контейнер
docker rm systech-aidd-postgres
docker rm systech-aidd-api
docker rm systech-aidd-bot
docker rm systech-aidd-frontend

# Или остановить все и запустить снова
make docker-down
make docker-up
```

### Проблема: Сборка не проходит
```bash
# Проверить Docker запущен
docker ps

# Проверить .env файл существует
ls -la .env

# Проверить место на диске
df -h

# Очистить Docker кэш
docker builder prune

# Пересобрать без кэша
docker compose -f devops/docker-compose.yml build --no-cache
```

### Проблема: Контейнер не запускается
```bash
# Посмотреть логи конкретного сервиса
docker compose -f devops/docker-compose.yml logs <service>

# Посмотреть последние 50 строк
docker compose -f devops/docker-compose.yml logs <service> --tail=50

# Следить за логами в реальном времени
docker compose -f devops/docker-compose.yml logs -f <service>
```

### Проблема: "Connection refused" при curl
```bash
# Проверить, что контейнеры запущены
make docker-ps

# Проверить, что прошло 30+ секунд после запуска
# (сервисам нужно время на инициализацию)

# Проверить логи на ошибки
make docker-logs | grep -i error
```

---

## 📚 Дополнительная информация

**Подробная документация:**
- `doc/guides/09-docker-deployment.md` - Полное руководство по Docker
- `doc/adrs/ADR-08.md` - Архитектурные решения
- `DOCKER-TEST-REPORT.md` - Отчёт о тестировании

**Makefile команды:**
```bash
make help                # Показать все доступные команды
make docker-build        # Собрать образы
make docker-up           # Запустить сервисы
make docker-down         # Остановить сервисы
make docker-ps           # Статус контейнеров
make docker-logs         # Просмотр логов
make docker-restart      # Перезапустить сервисы
make docker-clean        # Полная очистка
make docker-lint         # Hadolint проверка
make docker-scan         # Trivy security scan
```

---

## ✅ Критерии успеха

Проверка прошла успешно, если:

- ✅ Hadolint показал только warnings (не errors)
- ✅ Все 3 образа собрались без ошибок
- ✅ Все 4 контейнера в статусе "Up" (running)
- ✅ `curl http://localhost:8000/health` вернул `{"status":"ok"}`
- ✅ `curl http://localhost:3000/` вернул HTML
- ✅ В логах нет критичных ошибок (ERROR, FATAL)
- ✅ Bot показывает "Start polling"
- ✅ API показывает "Application startup complete"
- ✅ Frontend показывает "Ready in XXms"

---

**Время на полную проверку:** ~3-5 минут  
**Успешное прохождение:** Все пункты чек-листа выполнены без ошибок

**Удачи! 🚀**

