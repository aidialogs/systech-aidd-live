# Руководство по работе с CI/CD

## Обзор

Проект использует **GitHub Actions** для автоматической сборки и публикации Docker образов в GitHub Container Registry (ghcr.io).

**Что автоматизировано:**
- ✅ Сборка Docker образов при Pull Request (проверка)
- ✅ Публикация образов при push в тестовую ветку
- ✅ Кэширование для ускорения повторных сборок
- ✅ Тегирование образов (latest + commit SHA)

**Что НЕ автоматизировано (пока):**
- ❌ Запуск тестов в CI (планируется позже)
- ❌ Линтинг и проверка кода (планируется позже)
- ❌ Security scanning (планируется позже)
- ❌ Автоматический deploy на сервер (спринт D3)

## Структура CI/CD

```
.github/
└── workflows/
    └── build.yml          # Workflow для сборки и публикации образов
```

## Как работает workflow

### Триггеры

Workflow запускается автоматически при:

1. **Pull Request** → main или day6-ci-draft
   - Собирает образы (без публикации)
   - Проверяет, что образы собираются без ошибок
   - Результат отображается в PR

2. **Push** → day6-ci-draft
   - Собирает образы
   - Публикует в ghcr.io с тегами `latest` и `sha-abc1234`

### Процесс сборки

Для каждого сервиса (bot, api, frontend) параллельно:

1. **Checkout** — загрузка исходного кода
2. **Setup Buildx** — настройка Docker builder
3. **Cache** — загрузка кэша Docker layers
4. **Login** — аутентификация в ghcr.io (только для push)
5. **Metadata** — подготовка тегов и labels
6. **Build & Push** — сборка и публикация образа
7. **Summary** — отчет в GitHub Actions

**Время выполнения:**
- Первая сборка: ~5-10 минут (без кэша)
- Повторная сборка: ~2-5 минут (с кэшем)

## Работа с Pull Request

### Создание PR для проверки сборки

```bash
# 1. Создать ветку для изменений
git checkout -b feature/my-feature

# 2. Внести изменения
# ... редактировать файлы ...

# 3. Закоммитить и запушить
git add .
git commit -m "feat: Add new feature"
git push origin feature/my-feature

# 4. Создать PR через GitHub UI
# GitHub → Pull requests → New pull request
```

### Проверка статуса CI

После создания PR:

1. Откройте PR на GitHub
2. Внизу увидите секцию "Checks"
3. **Build and Push Docker Images** — статус workflow:
   - 🟡 Желтый — в процессе выполнения
   - ✅ Зеленый — сборка успешна
   - ❌ Красный — ошибка сборки

4. Кликните на "Details" чтобы увидеть логи

### Что проверяется в PR

- ✅ Образы bot, api, frontend собираются без ошибок
- ✅ Dockerfile синтаксически корректен
- ✅ Все необходимые файлы присутствуют

**Важно:** Образы собираются, но **НЕ публикуются** в registry при PR.

### Merge PR

После успешной проверки и ревью:

1. Убедитесь что все checks зеленые ✅
2. Получите approve от ревьюера (если требуется)
3. Нажмите **"Merge pull request"**
4. Выберите тип merge:
   - **Merge commit** — сохраняет всю историю
   - **Squash and merge** — объединяет коммиты в один
   - **Rebase and merge** — переносит коммиты

## Публикация образов

### Автоматическая публикация

Образы автоматически публикуются при push в ветку `day6-ci-draft`:

```bash
# Находясь на ветке day6-ci-draft
git add .
git commit -m "build: Update Docker images"
git push origin day6-ci-draft
```

**Что происходит:**
1. GitHub Actions запускает workflow
2. Собирает 3 образа параллельно (bot, api, frontend)
3. Публикует образы в ghcr.io:
   - `ghcr.io/<owner>/<repo>/bot:latest`
   - `ghcr.io/<owner>/<repo>/bot:sha-abc1234`
   - ... аналогично для api и frontend

### Проверка публикации

#### Через GitHub UI

1. GitHub → Actions → Workflows
2. Выбрать последний запуск "Build and Push Docker Images"
3. Проверить статус: должен быть ✅ зеленый
4. Кликнуть на job "build-and-push (bot/api/frontend)"
5. Посмотреть логи шага "Build and push Docker image"

#### Через GitHub Packages

1. GitHub → Packages (справа на главной странице репозитория)
2. Увидите 3 пакета: bot, api, frontend
3. Кликнуть на пакет → увидите теги (latest, sha-xxx)

#### Через Docker CLI

```bash
# Выйти из registry (если залогинены)
docker logout ghcr.io

# Попробовать скачать образ (если публичный)
docker pull ghcr.io/<owner>/<repo>/bot:latest
```

Если образ скачивается — публикация успешна! ✅

### Ручной запуск workflow (будущее улучшение)

В будущем можно добавить `workflow_dispatch` для ручного запуска:

```yaml
on:
  workflow_dispatch:
    inputs:
      tag:
        description: 'Tag to build'
        required: false
        default: 'latest'
```

Тогда можно будет запускать workflow через UI: Actions → Build and Push → Run workflow

## Использование образов локально

### Вариант 1: Через docker-compose (рекомендуется)

```bash
cd devops

# Загрузить образы из registry
make pull

# Запустить сервисы
make up-registry
```

### Вариант 2: Через docker-compose напрямую

```bash
cd devops

# Загрузить образы
docker compose -f docker-compose.registry.yml pull

# Запустить
docker compose -f docker-compose.registry.yml up
```

### Вариант 3: Отдельные команды docker

```bash
# Скачать образы
docker pull ghcr.io/<owner>/<repo>/bot:latest
docker pull ghcr.io/<owner>/<repo>/api:latest
docker pull ghcr.io/<owner>/<repo>/frontend:latest

# Запустить вручную (не рекомендуется, используйте docker-compose)
docker run -d --name bot ghcr.io/<owner>/<repo>/bot:latest
```

### Использование конкретного тега (SHA)

Если нужна конкретная версия:

```bash
# Посмотреть доступные теги на GitHub Packages
# Или в логах workflow

# Скачать конкретную версию
docker pull ghcr.io/<owner>/<repo>/bot:sha-abc1234
```

Изменить в `docker-compose.registry.yml`:
```yaml
bot:
  image: ghcr.io/<owner>/<repo>/bot:sha-abc1234  # Вместо latest
```

## Мониторинг и логи

### Просмотр логов workflow

1. GitHub → Actions
2. Выбрать workflow run
3. Кликнуть на job (например, "build-and-push (bot)")
4. Развернуть каждый step для деталей

**Полезные шаги для отладки:**
- "Checkout code" — проверка исходного кода
- "Build and push Docker image" — процесс сборки
- "Image build summary" — итоговая информация

### Типичные ошибки и решения

#### Ошибка: "dockerfile: not found"

**Причина:** Неправильный путь к Dockerfile.

**Решение:** Проверить `file:` в workflow и убедиться что Dockerfile существует.

#### Ошибка: "COPY failed: file not found"

**Причина:** В Dockerfile копируется файл, который не существует в context.

**Решение:**
1. Проверить что файл существует в репозитории
2. Проверить `.dockerignore` — файл может быть исключен
3. Проверить `context:` в workflow

#### Ошибка: "denied: permission_denied"

**Причина:** Недостаточно прав для публикации в ghcr.io.

**Решение:** Проверить `permissions` в workflow:
```yaml
permissions:
  contents: read
  packages: write
```

#### Ошибка: "rate limit exceeded"

**Причина:** Превышен лимит запросов к Docker Hub (при pull базовых образов).

**Решение:**
- Подождать 6 часов
- Или аутентифицироваться в Docker Hub (добавить секрет в GitHub)

#### Ошибка: Cache miss

**Не ошибка:** Первая сборка всегда без кэша. Повторные сборки будут быстрее.

## Оптимизация workflow

### Кэширование

Workflow использует GitHub Actions Cache для Docker layers:

```yaml
cache-from: type=gha,scope=${{ matrix.service }}
cache-to: type=gha,mode=max,scope=${{ matrix.service }}
```

**Преимущества:**
- ✅ Ускорение повторных сборок в 2-5 раз
- ✅ Автоматическое управление кэшем
- ✅ Отдельный кэш для каждого сервиса

**Ограничения:**
- Кэш сохраняется на 7 дней
- Максимум 10 GB на репозиторий

### Параллелизация

Workflow использует matrix strategy для параллельной сборки:

```yaml
strategy:
  matrix:
    service: [bot, api, frontend]
```

Это означает что все 3 образа собираются **одновременно**, а не последовательно.

**Время экономии:** ~3x быстрее чем последовательная сборка.

## Best Practices

### 1. Проверять сборку в PR перед merge

✅ Всегда создавайте PR и дожидайтесь зеленого статуса CI  
❌ Не пушьте напрямую в main без проверки

### 2. Использовать осмысленные commit messages

```bash
# Хорошо
git commit -m "feat: Add user authentication"
git commit -m "fix: Resolve database connection issue"
git commit -m "build: Update Dockerfile for bot service"

# Плохо
git commit -m "Update"
git commit -m "Fix stuff"
```

### 3. Делать образы публичными

После первой публикации сделайте образы публичными (см. [REGISTRY_SETUP.md](REGISTRY_SETUP.md))

Это упростит использование на серверах.

### 4. Периодически очищать старые версии

GitHub Packages хранит все версии образов. Удаляйте старые для экономии места:

1. GitHub → Packages → bot (или api/frontend)
2. Versions → выбрать старую версию
3. Delete this version

### 5. Использовать теги SHA для воспроизводимости

Для production deployment используйте конкретный SHA тег вместо `latest`:

```yaml
# Хорошо для production
image: ghcr.io/owner/repo/bot:sha-abc1234

# Плохо для production (может измениться)
image: ghcr.io/owner/repo/bot:latest
```

## Дальнейшие улучшения (будущие спринты)

### Что можно добавить в CI/CD:

- [ ] **Запуск тестов** — pytest в workflow
- [ ] **Линтинг** — ruff, mypy для Python; eslint для frontend
- [ ] **Security scanning** — Trivy или Snyk для поиска уязвимостей
- [ ] **Multi-platform builds** — сборка для arm64 и amd64
- [ ] **Semantic versioning** — автоматическое версионирование (v1.0.0)
- [ ] **Automatic deploy** — автоматическое развертывание на сервер (спринт D3)
- [ ] **Notifications** — уведомления в Telegram/Slack о статусе сборки
- [ ] **Release notes** — автогенерация changelog при релизе

### Оптимизация Dockerfile:

- [ ] **Multi-stage builds** — уменьшение размера образов
- [ ] **Layer optimization** — минимизация количества слоев
- [ ] **Security hardening** — non-root user, read-only filesystem

Эти улучшения будут добавлены постепенно по мере необходимости.

## Полезные команды

### Локальная проверка

```bash
# Собрать образ локально так же как в CI
docker build -f devops/Dockerfile.bot -t test-bot .

# Запустить локально
docker run --rm test-bot
```

### Проверка размера образов

```bash
# После pull из registry
docker images | grep ghcr.io

# Посмотреть размер
docker image inspect ghcr.io/<owner>/<repo>/bot:latest --format='{{.Size}}'
```

### Очистка локальных образов

```bash
# Удалить все образы из ghcr.io
docker images | grep ghcr.io | awk '{print $3}' | xargs docker rmi

# Очистка неиспользуемых образов
docker image prune -a
```

## FAQ

**Q: Как часто запускается workflow?**  
A: При каждом PR и при каждом push в `day6-ci-draft`.

**Q: Сколько времени занимает сборка?**  
A: 5-10 минут первая сборка, 2-5 минут повторная (с кэшем).

**Q: Можно ли отменить запущенный workflow?**  
A: Да, GitHub Actions → выбрать workflow → Cancel workflow.

**Q: Образы приватные или публичные?**  
A: По умолчанию приватные. Нужно сделать публичными вручную (см. REGISTRY_SETUP.md).

**Q: Где хранятся образы?**  
A: В GitHub Container Registry (ghcr.io) привязанном к репозиторию.

**Q: Как использовать образы на сервере?**  
A: Сделать образы публичными, затем `docker pull` на сервере. Подробнее в спринте D2.

**Q: Можно ли использовать другой registry (Docker Hub)?**  
A: Да, но ghcr.io интегрирован лучше и бесплатен для публичных репозиториев.

## Заключение

CI/CD workflow для проекта:

✅ Автоматически собирает образы при PR и push  
✅ Публикует в GitHub Container Registry  
✅ Использует кэширование для скорости  
✅ Тегирует образы для версионирования  
✅ Готов к расширению (тесты, deploy, и т.д.)  

Для вопросов и проблем создавайте GitHub Issues.

## Ссылки

- [GitHub Actions Intro](GITHUB_ACTIONS_INTRO.md) — введение в GitHub Actions
- [Registry Setup](REGISTRY_SETUP.md) — настройка публичного доступа
- [Docker Quickstart](DOCKER_QUICKSTART.md) — локальная работа с Docker
- [DevOps Roadmap](devops-roadmap.md) — план развития DevOps

