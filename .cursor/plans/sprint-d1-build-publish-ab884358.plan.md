<!-- ab884358-1ee6-4da2-b9a9-795a893bc0a9 d5bc0267-45e1-46ec-8bb7-fc10b2f14def -->
# Sprint D1: Build & Publish - План реализации

## Обзор

Автоматизация сборки Docker образов через GitHub Actions и публикация в GitHub Container Registry (ghcr.io) для репозитория `aidialogs/systech-aidd-live`. Фокус на простоте настройки и быстром запуске CI/CD.

## Цели спринта

1. Настроить GitHub Actions для автоматической сборки 3 образов
2. Опубликовать образы в ghcr.io с публичным доступом
3. Обеспечить версионирование через теги (latest + commit SHA)
4. Создать docker-compose.prod.yml для использования образов из registry
5. Документировать весь процесс на русском языке

## Компоненты реализации

### 1. Документация по GitHub Actions

**Файл:** `/devops/doc/guides/github-actions-intro.md`

Создать краткую инструкцию, включающую:

- **Основы GitHub Actions:**
                - Что такое workflow, jobs, steps
                - Синтаксис YAML для workflow файлов
                - Где хранятся workflows (`.github/workflows/`)

- **Триггеры (triggers):**
                - `push` - автоматический запуск при push в ветку
                - `pull_request` - запуск при создании/обновлении PR
                - `workflow_dispatch` - ручной запуск через UI
                - Фильтры по веткам и путям

- **Работа с Pull Requests:**
                - Как создать PR из feature-ветки
                - Автоматическая проверка сборки образов в PR
                - Merge только после успешного прохождения CI

- **GitHub Container Registry (ghcr.io):**
                - Что такое ghcr.io и как он работает
                - Public vs Private образы
                - Автоматическая авторизация через GITHUB_TOKEN
                - Формат образов: `ghcr.io/OWNER/IMAGE:TAG`

- **Секреты и токены:**
                - GITHUB_TOKEN - встроенный токен с правами на запись в ghcr.io
                - Permissions для workflow (packages: write, contents: read)

### 2. GitHub Actions Workflow

**Файл:** `.github/workflows/build-and-publish.yml`

**Структура workflow:**

```yaml
name: Build and Publish Docker Images

on:
  push:
    branches:
   - day06-smirnov-live-02-ci-pipeline
  pull_request:
    branches:
   - day06-smirnov-live-02-ci-pipeline
  workflow_dispatch:

permissions:
  contents: read
  packages: write

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service:
     - name: bot
            dockerfile: Dockerfile.backend
            context: .
            image_name: systech-aidd-bot
     - name: api
            dockerfile: Dockerfile.backend
            context: .
            image_name: systech-aidd-api
     - name: frontend
            dockerfile: Dockerfile.frontend
            context: .
            image_name: systech-aidd-frontend
```

**Ключевые шаги:**

1. **Checkout кода** - `actions/checkout@v4`
2. **Setup Docker Buildx** - `docker/setup-buildx-action@v3` (для кэширования)
3. **Login to ghcr.io** - `docker/login-action@v3` с GITHUB_TOKEN
4. **Extract metadata** - `docker/metadata-action@v5` для генерации тегов
5. **Build and push** - `docker/build-push-action@v5` с:

                        - Кэширование layers через `cache-from` и `cache-to`
                        - Теги: `latest` и `sha-<commit>`
                        - Push только при push в ветку (не в PR)

**Оптимизации:**

- Matrix strategy для параллельной сборки 3 образов
- Docker layer caching для ускорения повторных сборок
- Условный push (только при push, не в PR)

### 3. Настройка публичного доступа к образам

**После первого запуска workflow:**

1. Перейти на https://github.com/orgs/aidialogs/packages
2. Найти созданные образы (systech-aidd-bot, systech-aidd-api, systech-aidd-frontend)
3. Для каждого образа:

                        - Package settings → Change visibility → Public
                        - Убрать требование авторизации для pull

**Документация:** Добавить пошаговую инструкцию в `/devops/doc/guides/github-actions-intro.md`

### 4. docker-compose.prod.yml для registry образов

**Файл:** `/docker-compose.prod.yml`

Создать новый файл на основе `docker-compose.yml` с изменениями:

- Заменить `build` на `image: ghcr.io/aidialogs/IMAGE_NAME:latest`
- Для bot: `image: ghcr.io/aidialogs/systech-aidd-bot:latest`
- Для api: `image: ghcr.io/aidialogs/systech-aidd-api:latest`
- Для frontend: `image: ghcr.io/aidialogs/systech-aidd-frontend:latest`
- Сохранить все volumes, environment, depends_on без изменений
- Postgres остается без изменений (используется образ из Docker Hub)

**Команда для использования:**

```bash
docker compose -f docker-compose.prod.yml up -d
```

### 5. Makefile команды

**Добавить новые команды:**

```makefile
# Pull образов из registry
docker-pull:
	docker compose -f docker-compose.prod.yml pull

# Запуск с образами из registry
docker-prod-up:
	docker compose -f docker-compose.prod.yml up -d

# Остановка prod окружения
docker-prod-down:
	docker compose -f docker-compose.prod.yml down

# Логи prod окружения
docker-prod-logs:
	docker compose -f docker-compose.prod.yml logs -f
```

**Сохранить существующие команды** для локальной разработки (docker-up, docker-down, etc.)

### 6. Обновление devops-roadmap.md

**Файл:** `/devops/doc/devops-roadmap.md`

Обновить статус Sprint D1:

```markdown
| **D1** | Build & Publish | 🟢 Completed | [sprint-d1-build-publish.md](plans/sprint-d1-build-publish.md) |
```

### 7. План спринта

**Файл:** `/devops/doc/plans/sprint-d1-build-publish.md`

Создать детальный план (аналогично sprint-d0-docker-setup.md):

- Описание целей и задач
- Архитектурные решения
- Структура workflow
- Инструкции по настройке
- Критерии готовности
- Известные ограничения MVP
- Следующие шаги (Sprint D2)

### 8. Обновление README.md

**Файл:** `/README.md`

**Добавить секцию после "🔧 DevOps & Infrastructure":**

#### Badge статуса сборки

```markdown
[![Build and Publish](https://github.com/aidialogs/systech-aidd-live/actions/workflows/build-and-publish.yml/badge.svg?branch=day06-smirnov-live-02-ci-pipeline)](https://github.com/aidialogs/systech-aidd-live/actions/workflows/build-and-publish.yml)
```

#### Секция "🚢 Использование образов из Registry"

````markdown
## 🚢 Использование образов из GitHub Container Registry

Образы автоматически публикуются в ghcr.io после каждого commit в ветку `day06-smirnov-live-02-ci-pipeline`.

### Быстрый старт с готовыми образами

**1. Скачайте образы из registry:**
```bash
make docker-pull
````

**2. Запустите сервисы:**

```bash
make docker-prod-up
```

**3. Примените миграции (только при первом запуске):**

```bash
docker compose -f docker-compose.prod.yml exec api uv run alembic upgrade head
```

### Доступные образы

- `ghcr.io/aidialogs/systech-aidd-bot:latest` - Telegram bot
- `ghcr.io/aidialogs/systech-aidd-api:latest` - REST API
- `ghcr.io/aidialogs/systech-aidd-frontend:latest` - Web UI

Образы публичные - авторизация не требуется.

### Команды для работы с registry образами

| Команда | Описание |

|---------|----------|

| `make docker-pull` | Скачать образы из registry |

| `make docker-prod-up` | Запуск с образами из registry |

| `make docker-prod-down` | Остановка prod окружения |

| `make docker-prod-logs` | Просмотр логов |

### Локальная разработка vs Production образы

- **Локальная разработка:** `make docker-up` (сборка образов локально)
- **Production образы:** `make docker-prod-up` (использование образов из registry)

```

### 9. Тестирование

**Сценарии проверки:**

1. **Локальная проверка workflow:**

                        - Push в ветку `day06-smirnov-live-02-ci-pipeline`
                        - Проверить запуск workflow в GitHub Actions UI
                        - Убедиться что все 3 образа собираются параллельно
                        - Проверить успешную публикацию в ghcr.io

2. **Проверка PR:**

                        - Создать тестовый PR
                        - Убедиться что workflow запускается
                        - Проверить что образы собираются, но не публикуются (только в PR)

3. **Настройка публичного доступа:**

                        - Сделать все 3 образа публичными через GitHub UI
                        - Проверить доступность без авторизации

4. **Локальное использование образов:**
   ```bash
   make docker-pull
   make docker-prod-up
   docker compose -f docker-compose.prod.yml exec api uv run alembic upgrade head
   make docker-prod-logs
   # Проверить работоспособность всех сервисов
   make docker-prod-down
   ```

5. **Проверка тегов:**

                        - Убедиться что образы имеют теги `latest` и `sha-<commit>`
                        - Проверить возможность pull конкретной версии по SHA

## MVP ограничения

Следующие улучшения отложены на будущие спринты:

- ❌ Multi-platform builds (linux/amd64, linux/arm64)
- ❌ Security scanning (Trivy, Snyk)
- ❌ Lint checks (hadolint для Dockerfile)
- ❌ Automated tests в CI
- ❌ Multi-stage builds оптимизация
- ❌ Production builds для frontend
- ❌ Notifications в Telegram/Slack

## Ключевые файлы

### Создаваемые файлы:

- `.github/workflows/build-and-publish.yml` - GitHub Actions workflow
- `docker-compose.prod.yml` - docker-compose для registry образов
- `/devops/doc/guides/github-actions-intro.md` - введение в GitHub Actions
- `/devops/doc/plans/sprint-d1-build-publish.md` - план спринта

### Обновляемые файлы:

- `README.md` - badge, секция с registry образами
- `Makefile` - команды для работы с registry
- `/devops/doc/devops-roadmap.md` - статус Sprint D1

## Критерии готовности

- [ ] GitHub Actions workflow создан и работает
- [ ] Образы автоматически публикуются в ghcr.io при push
- [ ] Образы имеют теги latest и sha-<commit>
- [ ] Все 3 образа сделаны публичными
- [ ] docker-compose.prod.yml создан и протестирован
- [ ] Makefile команды добавлены и работают
- [ ] README обновлен с badge и инструкциями
- [ ] Документация создана (intro + plan)
- [ ] Локальная проверка успешна (pull + run)
- [ ] CI проверка работает в PR

### To-dos

- [ ] Создать документацию по GitHub Actions и Container Registry
- [ ] Создать .github/workflows/build-and-publish.yml с matrix strategy
- [ ] Создать docker-compose.prod.yml для образов из registry
- [ ] Добавить команды для работы с registry в Makefile
- [ ] Обновить README.md с badge и секцией по использованию образов
- [ ] Создать детальный план спринта в devops/doc/plans/
- [ ] Обновить статус Sprint D1 в devops-roadmap.md
- [ ] Протестировать workflow, публикацию образов и локальный pull