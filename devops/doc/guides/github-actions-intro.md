# Введение в GitHub Actions и Container Registry

## Обзор

Этот документ содержит краткое введение в GitHub Actions и GitHub Container Registry (ghcr.io) для автоматизации сборки и публикации Docker образов проекта systech-aidd-live.

## Основы GitHub Actions

### Что такое GitHub Actions?

GitHub Actions — это встроенная CI/CD платформа GitHub, которая позволяет автоматизировать процессы разработки: сборку, тестирование, деплой и другие задачи.

### Ключевые концепции

**Workflow (рабочий процесс):**
- YAML файл, описывающий автоматизированный процесс
- Хранится в репозитории по пути `.github/workflows/`
- Определяет когда, что и как выполнять

**Job (задача):**
- Набор шагов (steps), выполняемых на одном runner
- Может выполняться параллельно с другими jobs
- Пример: `build-and-publish`

**Step (шаг):**
- Отдельная команда или action
- Выполняются последовательно внутри job
- Примеры: checkout кода, сборка Docker образа

**Runner:**
- Виртуальная машина для выполнения jobs
- GitHub предоставляет hosted runners: `ubuntu-latest`, `windows-latest`, `macos-latest`

**Action:**
- Переиспользуемый компонент для выполнения задачи
- Примеры: `actions/checkout@v4`, `docker/build-push-action@v5`

### Синтаксис YAML для workflow

Базовая структура workflow файла:

```yaml
name: Название Workflow

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  job-name:
    runs-on: ubuntu-latest
    steps:
      - name: Название шага
        uses: action-name@version
        with:
          parameter: value
      
      - name: Выполнение команды
        run: echo "Hello World"
```

**Основные секции:**
- `name` - отображаемое имя workflow
- `on` - триггеры для запуска
- `jobs` - список задач для выполнения
- `runs-on` - тип runner для выполнения
- `steps` - последовательность шагов

## Триггеры (Triggers)

### Push - автоматический запуск при push

Запускает workflow при push коммитов в указанные ветки:

```yaml
on:
  push:
    branches:
      - main
      - develop
    paths:
      - 'src/**'
      - 'Dockerfile*'
```

**Использование:**
- Автоматическая сборка и публикация после merge
- Проверка что код в основной ветке всегда собирается

### Pull Request - запуск при создании/обновлении PR

Запускает workflow при создании или обновлении Pull Request:

```yaml
on:
  pull_request:
    branches:
      - main
```

**Использование:**
- Проверка что изменения в PR собираются без ошибок
- Валидация перед merge в основную ветку
- **Важно:** обычно без публикации артефактов (только сборка)

### Workflow Dispatch - ручной запуск

Позволяет запускать workflow вручную через GitHub UI:

```yaml
on:
  workflow_dispatch:
```

**Использование:**
- Деплой по требованию
- Тестирование без создания коммита
- Пересборка образов с теми же параметрами

### Комбинированные триггеры

Можно использовать несколько триггеров одновременно:

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
```

### Фильтры по путям

Запускать workflow только при изменении определенных файлов:

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'Dockerfile*'
      - '.github/workflows/**'
```

## Работа с Pull Requests

### Как создать Pull Request

1. **Создайте feature-ветку:**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Внесите изменения и закоммитьте:**
   ```bash
   git add .
   git commit -m "Add new feature"
   ```

3. **Push ветку в GitHub:**
   ```bash
   git push origin feature/my-feature
   ```

4. **Создайте PR через GitHub UI:**
   - Откройте репозиторий на GitHub
   - Нажмите "Pull requests" → "New pull request"
   - Выберите base ветку и compare ветку
   - Заполните описание и нажмите "Create pull request"

### Автоматическая проверка в PR

**Что происходит при создании PR:**
1. GitHub Actions автоматически запускает workflow
2. Выполняется сборка Docker образов (без публикации)
3. Статус отображается в PR (✅ зеленый или ❌ красный)
4. Блокировка merge если проверки не прошли (опционально)

**Почему в PR не публикуются образы:**
- Код еще не одобрен - нет смысла публиковать промежуточные версии
- Экономия места в registry - не засоряем образами из каждого PR
- Безопасность - публикуются только одобренные изменения

### Merge после успешного CI

**Best practice:**
1. Дождаться зеленого статуса всех проверок (✅)
2. Получить code review от коллег
3. Выполнить merge в основную ветку
4. После merge автоматически запустится workflow с публикацией образов

**Настройка branch protection (опционально):**
- Settings → Branches → Branch protection rules
- Require status checks to pass before merging
- Require branches to be up to date before merging

## GitHub Container Registry (ghcr.io)

### Что такое ghcr.io?

GitHub Container Registry — это встроенное хранилище Docker образов от GitHub.

**Преимущества:**
- ✅ Бесплатно для публичных репозиториев
- ✅ Интеграция с GitHub Actions (авторизация через GITHUB_TOKEN)
- ✅ Поддержка public и private образов
- ✅ Автоматическое версионирование и тегирование
- ✅ Связь образов с репозиторием и коммитами

### Формат образов

```
ghcr.io/OWNER/IMAGE_NAME:TAG
```

**Примеры для нашего проекта:**
```
ghcr.io/aidialogs/systech-aidd-bot:latest
ghcr.io/aidialogs/systech-aidd-api:latest
ghcr.io/aidialogs/systech-aidd-frontend:latest
ghcr.io/aidialogs/systech-aidd-bot:sha-a1b2c3d
```

**Компоненты:**
- `ghcr.io` - хост Container Registry
- `aidialogs` - владелец репозитория (organization или user)
- `systech-aidd-bot` - название образа
- `latest` / `sha-a1b2c3d` - тег (версия)

### Public vs Private образы

**Private (по умолчанию):**
- Доступны только с авторизацией
- Требуется `docker login ghcr.io` перед pull
- Подходит для закрытых проектов

**Public (рекомендуется для open source):**
- Доступны без авторизации
- `docker pull` работает сразу без логина
- Подходит для публичных проектов

**Как сделать образ публичным:**
1. Перейдите на https://github.com/orgs/aidialogs/packages
2. Найдите нужный образ (например, `systech-aidd-bot`)
3. Нажмите на образ → "Package settings"
4. Прокрутите вниз до "Danger Zone"
5. "Change visibility" → выберите "Public"
6. Подтвердите изменение

### Автоматическая авторизация в GitHub Actions

GitHub предоставляет встроенный токен `GITHUB_TOKEN` с правами на:
- Чтение кода репозитория
- Запись в GitHub Container Registry
- Создание комментариев и статусов

**Использование в workflow:**

```yaml
- name: Login to GitHub Container Registry
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

**Никаких дополнительных секретов не нужно!** `GITHUB_TOKEN` доступен автоматически.

## Секреты и токены

### GITHUB_TOKEN

**Что это:**
- Встроенный токен, автоматически создаваемый для каждого workflow run
- Имеет ограниченные права в пределах репозитория
- Действителен только во время выполнения workflow

**Доступ в workflow:**
```yaml
${{ secrets.GITHUB_TOKEN }}
```

**Права токена (настраиваются через permissions):**

```yaml
permissions:
  contents: read      # Чтение кода репозитория
  packages: write     # Запись в Container Registry
  pull-requests: write # Комментарии в PR (опционально)
```

### Настройка permissions для workflow

**Минимальные права для сборки и публикации образов:**

```yaml
permissions:
  contents: read    # Checkout кода
  packages: write   # Push образов в ghcr.io
```

**Почему важно ограничивать права:**
- Принцип минимальных привилегий (least privilege)
- Безопасность - workflow не может изменять код или настройки
- Явное указание что workflow может делать

## Версионирование и тегирование образов

### Стратегия тегирования

В нашем проекте используется две стратегии:

**1. Latest tag:**
- Всегда указывает на последнюю версию из основной ветки
- Удобно для разработки и быстрых обновлений
- `ghcr.io/aidialogs/systech-aidd-bot:latest`

**2. SHA tag (commit hash):**
- Привязан к конкретному коммиту
- Immutable - никогда не изменяется
- Позволяет откатиться на любую версию
- `ghcr.io/aidialogs/systech-aidd-bot:sha-a1b2c3d4`

### Примеры использования

**Разработка (latest):**
```bash
docker pull ghcr.io/aidialogs/systech-aidd-bot:latest
```

**Production (конкретная версия по SHA):**
```bash
docker pull ghcr.io/aidialogs/systech-aidd-bot:sha-a1b2c3d4
```

**Проверка истории версий:**
- Откройте страницу образа на GitHub
- Все теги отображаются с датами и коммитами
- Можно посмотреть что изменилось в каждой версии

## Типичный workflow для Docker образов

### Полный пример workflow

```yaml
name: Build and Publish Docker Images

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  packages: write

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    
    steps:
      # 1. Checkout кода
      - name: Checkout code
        uses: actions/checkout@v4
      
      # 2. Настройка Docker Buildx (для кэширования)
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      # 3. Авторизация в ghcr.io
      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      # 4. Извлечение метаданных (теги, labels)
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository_owner }}/my-image
          tags: |
            type=raw,value=latest
            type=sha,prefix=sha-
      
      # 5. Сборка и публикация
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./Dockerfile
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Объяснение ключевых шагов

**1. Checkout code:**
- Скачивает код репозитория в runner
- Без этого шага код недоступен для сборки

**2. Docker Buildx:**
- Расширенный builder для Docker
- Поддержка кэширования layers
- Multi-platform builds (опционально)

**3. Login to ghcr.io:**
- Авторизация для push образов
- Использует встроенный GITHUB_TOKEN

**4. Extract metadata:**
- Автоматическая генерация тегов и labels
- Поддержка семантического версионирования
- Связывание образа с коммитом и PR

**5. Build and push:**
- Сборка Docker образа
- Push только при push в ветку (не в PR!)
- Кэширование для ускорения повторных сборок

### Условный push (только при push, не в PR)

```yaml
push: ${{ github.event_name != 'pull_request' }}
```

**Логика:**
- `github.event_name == 'push'` → push = true → образ публикуется
- `github.event_name == 'pull_request'` → push = false → только сборка

## Matrix Strategy для параллельной сборки

### Зачем нужна matrix strategy?

Когда нужно собрать несколько образов с разными параметрами, можно:
- ❌ Дублировать steps для каждого образа (много кода)
- ✅ Использовать matrix strategy (параллельная сборка)

### Пример для 3 образов

```yaml
jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service:
          - name: bot
            dockerfile: Dockerfile.backend
            image_name: systech-aidd-bot
          - name: api
            dockerfile: Dockerfile.backend
            image_name: systech-aidd-api
          - name: frontend
            dockerfile: Dockerfile.frontend
            image_name: systech-aidd-frontend
    
    steps:
      - name: Build ${{ matrix.service.name }}
        uses: docker/build-push-action@v5
        with:
          file: ${{ matrix.service.dockerfile }}
          tags: ghcr.io/aidialogs/${{ matrix.service.image_name }}:latest
```

**Преимущества:**
- 3 job запускаются параллельно → быстрее
- Один код для всех образов → проще поддержка
- Легко добавить новый сервис → просто добавить в matrix

## Кэширование Docker layers

### Зачем нужно кэширование?

Docker сборка может занимать много времени:
- Установка зависимостей (apt, pip, npm)
- Загрузка пакетов из интернета
- Компиляция кода

**Кэширование ускоряет повторные сборки в 5-10 раз!**

### GitHub Actions Cache

```yaml
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**Как работает:**
- `cache-from` - использовать кэш из предыдущих сборок
- `cache-to` - сохранить layers для следующих сборок
- `mode=max` - кэшировать все промежуточные layers

**Пример ускорения:**
- Первая сборка: 5 минут
- Повторная сборка (без изменений): 30 секунд
- Сборка после изменения кода: 1-2 минуты

## Проверка статуса workflow

### В GitHub UI

1. Откройте репозиторий на GitHub
2. Перейдите на вкладку "Actions"
3. Выберите workflow "Build and Publish Docker Images"
4. Просмотрите список runs (запусков)
5. Кликните на run для просмотра деталей

**Статусы:**
- 🟡 Желтый - выполняется (in progress)
- ✅ Зеленый - успешно (success)
- ❌ Красный - ошибка (failure)
- ⚪ Серый - отменен (cancelled)

### В Pull Request

В каждом PR отображаются:
- Список проверок (checks)
- Статус каждой проверки
- Ссылка на детали workflow run

**Merge разрешен только если:**
- Все проверки прошли (✅)
- Или вручную проигнорированы ошибки

### Badge статуса в README

Добавьте badge для отображения статуса:

```markdown
[![Build Status](https://github.com/aidialogs/systech-aidd-live/actions/workflows/build-and-publish.yml/badge.svg)](https://github.com/aidialogs/systech-aidd-live/actions/workflows/build-and-publish.yml)
```

**Отображение:**
- 🟢 Passing - последний workflow прошел успешно
- 🔴 Failing - последний workflow завершился с ошибкой

## Полезные ссылки

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Container Registry Guide](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Docker Metadata Action](https://github.com/docker/metadata-action)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## Следующие шаги

После прочтения этого руководства вы готовы к:
1. Созданию workflow файла для проекта
2. Настройке автоматической сборки образов
3. Публикации образов в GitHub Container Registry
4. Работе с Pull Requests и проверками

См. также:
- [Sprint D1 Plan](../plans/sprint-d1-build-publish.md) - детальный план реализации
- [DevOps Roadmap](../devops-roadmap.md) - общий план DevOps процессов

