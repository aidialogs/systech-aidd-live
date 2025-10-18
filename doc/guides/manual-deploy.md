# Руководство по ручному развертыванию на сервер

## Содержание

1. [Введение](#введение)
2. [Предварительные требования](#предварительные-требования)
3. [Подготовка локально](#подготовка-локально)
4. [Подключение к серверу](#подключение-к-серверу)
5. [Подготовка сервера](#подготовка-сервера)
6. [Копирование файлов на сервер](#копирование-файлов-на-сервер)
7. [Загрузка Docker образов](#загрузка-docker-образов)
8. [Запуск сервисов](#запуск-сервисов)
9. [Запуск миграций базы данных](#запуск-миграций-базы-данных)
10. [Проверка работоспособности](#проверка-работоспособности)
11. [Управление сервисами](#управление-сервисами)
12. [Troubleshooting](#troubleshooting)
13. [Безопасность](#безопасность)
14. [Обновление приложения](#обновление-приложения)

---

## Введение

Это пошаговая инструкция для ручного развертывания приложения **systech-aidd-live** на удаленном сервере с использованием Docker Compose и предсобранных образов из GitHub Container Registry (ghcr.io).

**Архитектура:**
- **PostgreSQL** - база данных
- **Bot** - Telegram бот (aiogram)
- **API** - FastAPI REST API
- **Frontend** - Next.js веб-интерфейс

**Все сервисы запускаются в Docker контейнерах** и управляются через Docker Compose.

---

## Предварительные требования

### На локальной машине

- ✅ SSH доступ к серверу по ключу
- ✅ SSH ключ: `/Users/akozhin/projects/ai/ai-devops/systech/devops/keys/systech_admin_key`
- ✅ Git репозиторий проекта клонирован
- ✅ Утилита `scp` для копирования файлов

### На сервере

- ✅ **IP адрес:** 90.156.229.75
- ✅ **OS:** Linux (любой дистрибутив с Docker)
- ✅ **Docker:** версия 20.10+ установлен
- ✅ **Docker Compose:** версия 2.0+ установлен
- ✅ **SSH доступ:** по ключу настроен
- ⚠️ **Порты открыты:** 22 (SSH), 3000 (Frontend), 8000 (API)

### Секреты и токены

Вам потребуются:
- 🔒 **BOT_TOKEN** - токен Telegram бота (от @BotFather)
- 🔒 **LLM_API_KEY** - API ключ для LLM сервиса (OpenRouter/OpenAI)
- 🔒 **POSTGRES_PASSWORD** - сильный пароль для PostgreSQL (минимум 16 символов)

---

## Подготовка локально

### Шаг 1: Перейти в директорию devops

```bash
cd /Users/akozhin/projects/systech-aidd-live/devops
```

### Шаг 2: Создать production .env файл

Скопируйте шаблон и заполните реальными значениями:

```bash
cp .env.production.example .env
nano .env  # или используйте любой редактор
```

**Обязательно замените:**
- `BOT_TOKEN=your_bot_token_here` → ваш реальный токен
- `LLM_API_KEY=your_api_key_here` → ваш реальный ключ
- `POSTGRES_PASSWORD=CHANGE_THIS_PASSWORD` → сильный пароль (16+ символов)
- `DATABASE_URL=...CHANGE_THIS_PASSWORD@...` → тот же пароль

**Пример сильного пароля:**
```bash
openssl rand -base64 32
# Результат: XyZ12ABc...34DEfgh56...
```

**Проверьте что переменная `NEXT_PUBLIC_API_URL` указана правильно:**
```bash
NEXT_PUBLIC_API_URL=http://90.156.229.75:8000
```

### Шаг 3: Установить права на .env файл

```bash
chmod 600 .env
```

### Шаг 4: Проверить docker-compose.prod.yml

Убедитесь что файл `docker-compose.prod.yml` существует:

```bash
ls -lh docker-compose.prod.yml
cat docker-compose.prod.yml  # просмотр содержимого
```

**Важные параметры в файле:**
- Образы: `ghcr.io/aidialogs/systech-aidd-live/{bot,api,frontend}:latest`
- PostgreSQL: порты НЕ публикуются (безопасность)
- Restart policy: `always`

### Шаг 5: Создать бэкап .env

**⚠️ КРИТИЧНО:** Сохраните копию .env в безопасном месте!

```bash
# Вариант 1: Сохранить локально
cp .env .env.backup
mv .env.backup ~/secure/systech-aidd.env.backup

# Вариант 2: Записать в password manager (рекомендуется)
# Скопируйте содержимое .env в KeePass, 1Password, LastPass и т.д.
```

---

## Подключение к серверу

### Проверка SSH доступа

```bash
ssh -i /Users/akozhin/projects/ai/ai-devops/systech/devops/keys/systech_admin_key root@90.156.229.75
```

**Если всё работает, вы увидите приглашение командной строки сервера:**
```
root@server:~#
```

### Проверка Docker на сервере

После подключения выполните:

```bash
docker --version
# Ожидается: Docker version 28.5.1 или выше

docker compose version
# Ожидается: Docker Compose version v2.40.1 или выше

docker ps
# Ожидается: список контейнеров (может быть пустым)
```

**Если всё OK, выйдите из SSH:**
```bash
exit
```

---

## Подготовка сервера

### Шаг 1: Создать директорию для приложения

Подключитесь к серверу и создайте структуру директорий:

```bash
ssh -i /Users/akozhin/projects/ai/ai-devops/systech/devops/keys/systech_admin_key root@90.156.229.75
```

На сервере выполните:

```bash
# Создаем директорию
mkdir -p /opt/systech-aidd

# Переходим в неё
cd /opt/systech-aidd

# Проверяем
pwd
# Ожидается: /opt/systech-aidd
```

### Шаг 2: Проверить открытые порты

⚠️ **КРИТИЧНО:** Для работы приложения необходимо открыть порты:

```bash
# На сервере проверяем firewall (если используется)
# Для Ubuntu/Debian с ufw:
ufw status

# Открываем порты (если закрыты):
ufw allow 3000/tcp  # Frontend
ufw allow 8000/tcp  # API
ufw allow 22/tcp    # SSH (должен быть уже открыт)

# НЕ открываем 5432 (PostgreSQL) - только внутри Docker!

# Перезагружаем firewall
ufw reload
```

**Для других firewall (iptables, firewalld):** обратитесь к документации вашего дистрибутива.

**Проверка открытых портов локально:**

Откройте новый терминал на локальной машине:

```bash
nc -zv -w 3 90.156.229.75 22
nc -zv -w 3 90.156.229.75 3000
nc -zv -w 3 90.156.229.75 8000
```

Все три должны вернуть `succeeded`.

### Шаг 3: Остаться в директории /opt/systech-aidd

```bash
# На сервере, убедитесь что вы в правильной директории
cd /opt/systech-aidd
```

**Не выходите из SSH**, мы будем копировать файлы.

---

## Копирование файлов на сервер

**Откройте НОВЫЙ терминал** на локальной машине (оставьте SSH сессию открытой).

### Шаг 1: Копировать docker-compose.prod.yml

```bash
cd /Users/akozhin/projects/systech-aidd-live/devops

scp -i /Users/akozhin/projects/ai/ai-devops/systech/devops/keys/systech_admin_key \
    docker-compose.prod.yml \
    root@90.156.229.75:/opt/systech-aidd/docker-compose.yml
```

**Примечание:** Переименовываем в `docker-compose.yml` для удобства (не нужно указывать `-f` каждый раз).

### Шаг 2: Копировать .env файл

```bash
scp -i /Users/akozhin/projects/ai/ai-devops/systech/devops/keys/systech_admin_key \
    .env \
    root@90.156.229.75:/opt/systech-aidd/.env
```

### Шаг 3: Копировать скрипт проверки (опционально)

```bash
scp -i /Users/akozhin/projects/ai/ai-devops/systech/devops/keys/systech_admin_key \
    deploy-check.sh \
    root@90.156.229.75:/opt/systech-aidd/deploy-check.sh
```

### Шаг 4: Проверить скопированные файлы

Вернитесь в SSH терминал (где открыта сессия на сервере):

```bash
# На сервере
cd /opt/systech-aidd
ls -lah

# Ожидается:
# -rw-r--r-- 1 root root  docker-compose.yml
# -rw------- 1 root root  .env
# -rwxr-xr-x 1 root root  deploy-check.sh (если скопировали)
```

### Шаг 5: Установить правильные права на .env

```bash
# На сервере
chmod 600 .env
chown root:root .env
```

### Шаг 6: Проверить содержимое файлов

```bash
# Проверяем что файлы не повреждены
head -5 docker-compose.yml
head -5 .env

# Проверяем что секреты на месте (но НЕ показываем в терминале!)
grep -c "BOT_TOKEN=" .env
# Ожидается: 1 или больше

grep -c "LLM_API_KEY=" .env
# Ожидается: 1 или больше
```

---

## Загрузка Docker образов

**На сервере** (в SSH сессии):

### Шаг 1: Перейти в директорию приложения

```bash
cd /opt/systech-aidd
```

### Шаг 2: Загрузить образы из ghcr.io

```bash
docker compose pull
```

**Процесс займет 2-5 минут** в зависимости от скорости сети.

**Вы увидите:**
```
[+] Pulling 4/4
 ✔ postgres Pulled
 ✔ bot Pulled
 ✔ api Pulled
 ✔ frontend Pulled
```

### Шаг 3: Проверить загруженные образы

```bash
docker images | grep systech-aidd
docker images | grep postgres
```

**Ожидается:**
```
ghcr.io/aidialogs/systech-aidd-live/bot        latest   ...
ghcr.io/aidialogs/systech-aidd-live/api        latest   ...
ghcr.io/aidialogs/systech-aidd-live/frontend   latest   ...
postgres                                       16-alpine ...
```

**Если образы не загружаются (ошибка 401/403):**
- Проверьте что образы публичные (см. [Troubleshooting](#troubleshooting))

---

## Запуск сервисов

### Шаг 1: Запустить все сервисы

```bash
# На сервере
cd /opt/systech-aidd

docker compose up -d
```

**Флаг `-d`** = detached mode (фоновый режим).

**Процесс займет 30-60 секунд.** Docker:
1. Создаст volumes для данных
2. Создаст сеть systech-network
3. Запустит контейнеры в правильном порядке (postgres → bot/api → frontend)

**Вы увидите:**
```
[+] Running 5/5
 ✔ Network systech-network        Created
 ✔ Container systech-aidd-postgres Started
 ✔ Container systech-aidd-bot      Started
 ✔ Container systech-aidd-api      Started
 ✔ Container systech-aidd-frontend Started
```

### Шаг 2: Проверить статус контейнеров

```bash
docker compose ps
```

**Ожидается:**
```
NAME                   STATUS         PORTS
systech-aidd-postgres  Up 10 seconds  
systech-aidd-bot       Up 5 seconds   
systech-aidd-api       Up 5 seconds   0.0.0.0:8000->8000/tcp
systech-aidd-frontend  Up 5 seconds   0.0.0.0:3000->3000/tcp
```

**Все должны быть в статусе `Up`.** Если что-то в `Exited` или `Restarting` - см. [Troubleshooting](#troubleshooting).

### Шаг 3: Посмотреть логи

```bash
# Логи всех сервисов (последние 50 строк)
docker compose logs --tail=50

# Логи конкретного сервиса
docker compose logs --tail=50 api
docker compose logs --tail=50 bot
docker compose logs --tail=50 frontend
docker compose logs --tail=50 postgres

# Следить за логами в реальном времени
docker compose logs -f api
# Выйти: Ctrl+C
```

**Ищем в логах:**
- ✅ `Application startup complete` (API)
- ✅ `Bot started successfully` или `Polling started` (Bot)
- ✅ `Ready started` (Frontend)
- ✅ Нет ошибок типа `ERROR`, `CRITICAL`, `Fatal`

---

## Запуск миграций базы данных

⚠️ **КРИТИЧНО:** Перед использованием приложения необходимо применить миграции БД.

### Шаг 1: Дождаться готовности PostgreSQL

```bash
# На сервере
docker compose exec postgres pg_isready -U systech_user -d systech_aidd
```

**Ожидается:**
```
/var/run/postgresql:5432 - accepting connections
```

Если `no response` - подождите 10-20 секунд и повторите.

### Шаг 2: Применить миграции Alembic

```bash
docker compose exec api alembic upgrade head
```

**Ожидается:**
```
INFO  [alembic.runtime.migration] Running upgrade -> <revision>, <description>
INFO  [alembic.runtime.migration] Running upgrade <revision> -> <revision>, <description>
...
```

**Если ошибка `alembic: command not found`:**
- Убедитесь что контейнер api запущен: `docker compose ps api`
- Проверьте логи: `docker compose logs api`

### Шаг 3: Проверить таблицы в БД

```bash
docker compose exec postgres psql -U systech_user -d systech_aidd -c "\dt"
```

**Ожидается:**
```
             List of relations
 Schema |      Name       | Type  |    Owner     
--------+-----------------+-------+--------------
 public | alembic_version | table | systech_user
 public | messages        | table | systech_user
 public | users           | table | systech_user
```

---

## Проверка работоспособности

### Автоматическая проверка (рекомендуется)

Если вы скопировали `deploy-check.sh`:

```bash
# На сервере
cd /opt/systech-aidd
chmod +x deploy-check.sh
./deploy-check.sh
```

Скрипт автоматически проверит все сервисы и выведет отчет.

### Ручная проверка

#### 1. Проверка контейнеров

```bash
docker compose ps
```

Все 4 сервиса должны быть `Up`.

#### 2. Проверка PostgreSQL

```bash
docker compose exec postgres pg_isready -U systech_user -d systech_aidd
```

Ожидается: `accepting connections`

#### 3. Проверка API Health

```bash
curl http://localhost:8000/health
```

**Ожидается:**
```json
{"status":"healthy"}
```

#### 4. Проверка API Docs

```bash
curl -I http://localhost:8000/docs
```

Ожидается: `HTTP/1.1 200 OK`

**Или откройте в браузере:**
```
http://90.156.229.75:8000/docs
```

#### 5. Проверка Frontend

```bash
curl -I http://localhost:3000
```

Ожидается: `HTTP/1.1 200 OK`

**Или откройте в браузере:**
```
http://90.156.229.75:3000
```

#### 6. Проверка Telegram Bot

Откройте Telegram, найдите вашего бота и отправьте команду:
```
/start
```

**Ожидается:** Бот должен ответить приветственным сообщением.

#### 7. Проверка логов

```bash
# Проверяем что нет критичных ошибок
docker compose logs --tail=100 | grep -i error
docker compose logs --tail=100 | grep -i fatal
docker compose logs --tail=100 | grep -i critical
```

**Если вывод пустой** - отлично, ошибок нет.

#### 8. Проверка использования ресурсов

```bash
docker stats --no-stream
```

**Ожидается:** Все контейнеры используют <50% CPU и <512MB RAM.

---

## Управление сервисами

### Просмотр логов

```bash
# Все сервисы
docker compose logs -f

# Конкретный сервис
docker compose logs -f api
docker compose logs -f bot
docker compose logs -f frontend
docker compose logs -f postgres

# Последние N строк
docker compose logs --tail=100 api

# С временными метками
docker compose logs -f -t api
```

### Перезапуск сервисов

```bash
# Перезапуск всех
docker compose restart

# Перезапуск конкретного сервиса
docker compose restart api
docker compose restart bot
```

### Остановка сервисов

```bash
# Остановка без удаления контейнеров
docker compose stop

# Остановка и удаление контейнеров (данные сохраняются в volumes)
docker compose down

# Остановка с удалением volumes (⚠️ УДАЛИТ ВСЕ ДАННЫЕ БД!)
docker compose down -v  # НЕ используйте без необходимости!
```

### Запуск сервисов

```bash
# Запуск (если остановлены)
docker compose start

# Запуск с пересозданием контейнеров
docker compose up -d --force-recreate
```

### Доступ к контейнеру

```bash
# Shell в контейнер API
docker compose exec api bash

# Shell в контейнер Bot
docker compose exec bot bash

# PostgreSQL CLI
docker compose exec postgres psql -U systech_user -d systech_aidd

# Выполнить команду в контейнере
docker compose exec api python --version
```

### Просмотр статуса

```bash
# Статус контейнеров
docker compose ps

# Детальная информация
docker compose ps -a

# Использование ресурсов
docker stats
```

---

## Troubleshooting

### Проблема: Контейнер не запускается (Exited)

**Симптомы:**
```bash
docker compose ps
# systech-aidd-bot  Exited (1) 2 seconds ago
```

**Решение:**

1. Посмотреть логи:
   ```bash
   docker compose logs bot
   ```

2. Проверить что .env файл правильный:
   ```bash
   cat .env | grep BOT_TOKEN
   cat .env | grep DATABASE_URL
   ```

3. Проверить что все переменные заполнены (нет `your_*_here`)

4. Перезапустить контейнер:
   ```bash
   docker compose restart bot
   ```

### Проблема: API недоступен (Connection refused)

**Симптомы:**
```bash
curl http://localhost:8000/health
# curl: (7) Failed to connect to localhost port 8000: Connection refused
```

**Решение:**

1. Проверить что контейнер запущен:
   ```bash
   docker compose ps api
   ```

2. Проверить логи API:
   ```bash
   docker compose logs api
   ```

3. Проверить что порт 8000 слушается:
   ```bash
   netstat -tlnp | grep 8000
   # или
   ss -tlnp | grep 8000
   ```

4. Проверить firewall:
   ```bash
   ufw status | grep 8000
   ```

5. Перезапустить API:
   ```bash
   docker compose restart api
   ```

### Проблема: Frontend не загружается

**Симптомы:**
```bash
curl http://localhost:3000
# curl: (7) Failed to connect
```

**Решение:**

1. Проверить логи Frontend:
   ```bash
   docker compose logs frontend
   ```

2. Проверить переменную NEXT_PUBLIC_API_URL:
   ```bash
   docker compose exec frontend env | grep NEXT_PUBLIC_API_URL
   # Ожидается: http://90.156.229.75:8000
   ```

3. Перезапустить Frontend:
   ```bash
   docker compose restart frontend
   ```

### Проблема: Bot не отвечает в Telegram

**Симптомы:**
- Бот не отвечает на /start
- В Telegram бот показывается офлайн

**Решение:**

1. Проверить логи Bot:
   ```bash
   docker compose logs bot
   ```

2. Проверить BOT_TOKEN:
   ```bash
   docker compose exec bot env | grep BOT_TOKEN
   # НЕ показывайте токен публично!
   ```

3. Проверить что токен валидный (через @BotFather):
   - Telegram → @BotFather → /mybots → выбрать бота → API Token

4. Перезапустить Bot:
   ```bash
   docker compose restart bot
   ```

### Проблема: PostgreSQL недоступен

**Симптомы:**
```bash
docker compose exec postgres pg_isready
# no response
```

**Решение:**

1. Проверить логи PostgreSQL:
   ```bash
   docker compose logs postgres
   ```

2. Проверить что контейнер запущен:
   ```bash
   docker compose ps postgres
   ```

3. Проверить health check:
   ```bash
   docker inspect systech-aidd-postgres | grep -A 10 Health
   ```

4. Перезапустить PostgreSQL:
   ```bash
   docker compose restart postgres
   # Подождать 10-20 секунд
   docker compose exec postgres pg_isready
   ```

### Проблема: Ошибка миграций Alembic

**Симптомы:**
```bash
docker compose exec api alembic upgrade head
# ERROR: ...
```

**Решение:**

1. Проверить что PostgreSQL доступен:
   ```bash
   docker compose exec postgres pg_isready
   ```

2. Проверить DATABASE_URL:
   ```bash
   docker compose exec api env | grep DATABASE_URL
   ```

3. Проверить что пароль в DATABASE_URL совпадает с POSTGRES_PASSWORD

4. Посмотреть текущую версию БД:
   ```bash
   docker compose exec postgres psql -U systech_user -d systech_aidd \
       -c "SELECT version_num FROM alembic_version;"
   ```

5. Попробовать откатить и применить снова:
   ```bash
   docker compose exec api alembic downgrade -1
   docker compose exec api alembic upgrade head
   ```

### Проблема: Образы не загружаются (unauthorized)

**Симптомы:**
```bash
docker compose pull
# Error response: unauthorized: ...
```

**Решение:**

**Вариант 1: Сделать образы публичными (рекомендуется)**

На локальной машине:
1. Перейти на GitHub → Packages
2. Выбрать каждый образ (bot, api, frontend)
3. Package settings → Change visibility → Public
4. Подтвердить

Затем на сервере:
```bash
docker compose pull
```

**Вариант 2: Авторизоваться с Personal Access Token**

На сервере:
```bash
# Создать PAT на GitHub с правами read:packages
# GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token

docker login ghcr.io -u YOUR_GITHUB_USERNAME
# Password: введите PAT (не обычный пароль!)

docker compose pull
```

### Проблема: Недостаточно места на диске

**Симптомы:**
```bash
docker compose up -d
# Error: no space left on device
```

**Решение:**

1. Проверить использование диска:
   ```bash
   df -h
   ```

2. Очистить неиспользуемые Docker ресурсы:
   ```bash
   docker system prune -a --volumes
   # ⚠️ Удалит ВСЕ неиспользуемые образы и volumes!
   ```

3. Удалить старые образы:
   ```bash
   docker images
   docker rmi <IMAGE_ID>
   ```

### Проблема: Порты заняты

**Симптомы:**
```bash
docker compose up -d
# Error: port is already allocated
```

**Решение:**

1. Найти процесс использующий порт:
   ```bash
   sudo lsof -i :8000
   sudo lsof -i :3000
   ```

2. Остановить процесс:
   ```bash
   sudo kill <PID>
   ```

3. Или изменить порты в docker-compose.yml:
   ```yaml
   ports:
     - "8001:8000"  # вместо 8000:8000
   ```

---

## Безопасность

### Рекомендации

1. **Защита .env файла:**
   ```bash
   chmod 600 .env
   chown root:root .env
   ```

2. **Firewall:**
   ```bash
   # Открыть только необходимые порты
   ufw allow 22/tcp   # SSH
   ufw allow 3000/tcp # Frontend
   ufw allow 8000/tcp # API
   ufw enable
   ```

3. **SSH ключ:**
   ```bash
   # На локальной машине
   chmod 600 /Users/akozhin/projects/ai/ai-devops/systech/devops/keys/systech_admin_key
   ```

4. **Сильные пароли:**
   - PostgreSQL: минимум 16 символов, включая спецсимволы
   - Генерация: `openssl rand -base64 32`

5. **Регулярные обновления:**
   ```bash
   # На сервере
   apt update && apt upgrade -y  # Ubuntu/Debian
   docker system prune -f        # Очистка старых образов
   ```

6. **Мониторинг логов:**
   ```bash
   # Настроить logrotate для Docker логов
   nano /etc/docker/daemon.json
   ```
   ```json
   {
     "log-driver": "json-file",
     "log-opts": {
       "max-size": "10m",
       "max-file": "3"
     }
   }
   ```

7. **Бэкапы базы данных:**
   ```bash
   # Ежедневный бэкап
   docker compose exec postgres pg_dump -U systech_user systech_aidd > backup_$(date +%Y%m%d).sql
   
   # Восстановление
   docker compose exec -T postgres psql -U systech_user -d systech_aidd < backup_20251018.sql
   ```

8. **Не храните секреты в git:**
   ```bash
   # В .gitignore должно быть:
   .env
   .env.production
   .env.local
   ```

---

## Обновление приложения

### Обновление до последней версии

1. **Загрузить новые образы:**
   ```bash
   cd /opt/systech-aidd
   docker compose pull
   ```

2. **Применить миграции (если есть):**
   ```bash
   docker compose exec api alembic upgrade head
   ```

3. **Перезапустить сервисы:**
   ```bash
   docker compose up -d
   ```

4. **Проверить что всё работает:**
   ```bash
   docker compose ps
   docker compose logs -f --tail=50
   ```

### Откат к предыдущей версии

Если используются SHA теги:

1. **Изменить docker-compose.yml:**
   ```yaml
   # Вместо :latest используйте конкретный SHA
   image: ghcr.io/aidialogs/systech-aidd-live/api:sha-abc1234
   ```

2. **Перезапустить:**
   ```bash
   docker compose up -d
   ```

### Zero-downtime deployment (без простоя)

Для production рекомендуется использовать:
- Blue-Green deployment
- Rolling updates
- Health checks перед переключением

Эти механизмы будут реализованы в **Спринте D3: Auto Deploy**.

---

## Полезные команды

### Docker Compose

```bash
# Запуск
docker compose up -d

# Остановка
docker compose down

# Перезапуск
docker compose restart

# Логи
docker compose logs -f

# Статус
docker compose ps

# Обновление
docker compose pull && docker compose up -d
```

### Проверка

```bash
# Health checks
curl http://localhost:8000/health
curl http://localhost:3000/

# PostgreSQL
docker compose exec postgres pg_isready

# Миграции
docker compose exec api alembic current
docker compose exec api alembic upgrade head
```

### Мониторинг

```bash
# Использование ресурсов
docker stats

# Логи в реальном времени
docker compose logs -f api

# Disk usage
docker system df
```

### Очистка

```bash
# Удалить остановленные контейнеры
docker container prune

# Удалить неиспользуемые образы
docker image prune -a

# Удалить всё неиспользуемое
docker system prune -a
```

---

## Итоговый чеклист

После выполнения всех шагов, убедитесь что:

- ✅ Все 4 контейнера запущены (`docker compose ps`)
- ✅ PostgreSQL health check проходит
- ✅ API доступен: `http://90.156.229.75:8000/docs`
- ✅ Frontend доступен: `http://90.156.229.75:3000`
- ✅ Bot отвечает в Telegram на `/start`
- ✅ Миграции БД применены
- ✅ Логи без критичных ошибок
- ✅ .env файл защищен (chmod 600)
- ✅ Создан бэкап .env в безопасном месте
- ✅ Порты 3000 и 8000 открыты в firewall

---

## Что дальше?

После успешного развертывания:

1. **Настроить мониторинг** (опционально)
   - Prometheus + Grafana
   - Uptime monitoring (UptimeRobot, Pingdom)

2. **Настроить автоматические бэкапы БД**
   - Cron job для ежедневных бэкапов
   - Хранение в S3 / Google Cloud Storage

3. **Настроить SSL/TLS** (рекомендуется)
   - Nginx reverse proxy
   - Let's Encrypt сертификаты
   - HTTPS для API и Frontend

4. **Подготовиться к Спринту D3**
   - Auto Deploy через GitHub Actions
   - Автоматический rollback при ошибках
   - Notifications в Telegram/Slack

---

## Полезные ссылки

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Backup & Restore](https://www.postgresql.org/docs/current/backup.html)
- [Nginx Reverse Proxy Guide](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Let's Encrypt](https://letsencrypt.org/)

---

**Документ создан:** 18 октября 2025  
**Версия:** 1.0  
**Статус:** Production Ready ✅

