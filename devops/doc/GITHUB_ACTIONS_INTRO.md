# Введение в GitHub Actions

## Что такое GitHub Actions?

**GitHub Actions** — это платформа для автоматизации процессов разработки (CI/CD) прямо в репозитории GitHub. Позволяет автоматически выполнять задачи при определенных событиях (push, pull request, создание релиза и т.д.).

## Основные концепции

### Workflow (Рабочий процесс)

**Workflow** — это автоматизированный процесс, состоящий из одной или нескольких задач (jobs). Описывается в YAML файле в директории `.github/workflows/`.

Пример структуры:
```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Hello World"
```

### Events (События)

**Events** — триггеры, которые запускают workflow:

- `push` — при push коммита в ветку
- `pull_request` — при создании/обновлении PR
- `workflow_dispatch` — ручной запуск через UI GitHub
- `schedule` — по расписанию (cron)
- `release` — при создании релиза

Примеры:
```yaml
# Запуск при push в main
on:
  push:
    branches: [main]

# Запуск при любом PR
on:
  pull_request:

# Комбинация событий
on:
  push:
    branches: [main, develop]
  pull_request:
  workflow_dispatch:
```

### Jobs (Задачи)

**Job** — набор шагов (steps), выполняемых на одном runner'е. Jobs выполняются параллельно по умолчанию, но можно настроить зависимости.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Build
        run: npm run build

  test:
    needs: build  # Зависимость от job build
    runs-on: ubuntu-latest
    steps:
      - run: npm test
```

### Steps (Шаги)

**Step** — отдельная команда или action в рамках job. Выполняются последовательно.

Два типа шагов:
1. **Action** — готовое действие (uses):
   ```yaml
   - uses: actions/checkout@v4
   ```

2. **Command** — shell команда (run):
   ```yaml
   - run: echo "Hello"
   ```

### Runners (Исполнители)

**Runner** — виртуальная машина, на которой выполняется workflow.

GitHub предоставляет бесплатные runners:
- `ubuntu-latest` — Ubuntu Linux (рекомендуется)
- `windows-latest` — Windows
- `macos-latest` — macOS

## Matrix Strategy (Матричная стратегия)

**Matrix** позволяет запускать job несколько раз с разными параметрами параллельно.

Пример — сборка для разных версий Python:
```yaml
jobs:
  test:
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    steps:
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
```

Пример — сборка нескольких Docker образов:
```yaml
jobs:
  build:
    strategy:
      matrix:
        service: [bot, api, frontend]
    steps:
      - name: Build ${{ matrix.service }}
        run: docker build -t ${{ matrix.service }} .
```

Matrix автоматически создает 3 параллельных job'а (по одному для каждого service).

## Docker и GitHub Container Registry

### GitHub Container Registry (ghcr.io)

**ghcr.io** — публичный/приватный Docker registry от GitHub. Интегрирован с GitHub Actions.

Преимущества:
- Бесплатный для публичных репозиториев
- Автоматическая аутентификация через `GITHUB_TOKEN`
- Привязка образов к репозиторию
- Контроль доступа через GitHub permissions

### Публикация образов в ghcr.io

Базовый процесс:

1. **Login в registry:**
   ```yaml
   - name: Login to GitHub Container Registry
     uses: docker/login-action@v3
     with:
       registry: ghcr.io
       username: ${{ github.actor }}
       password: ${{ secrets.GITHUB_TOKEN }}
   ```

2. **Build и Push образа:**
   ```yaml
   - name: Build and push
     uses: docker/build-push-action@v5
     with:
       context: .
       push: true
       tags: ghcr.io/${{ github.repository }}/myapp:latest
   ```

### Публичные vs Приватные образы

**Приватные образы** (по умолчанию):
- Требуют аутентификацию для pull
- Видны только участникам репозитория
- Используются для внутренних проектов

**Публичные образы**:
- Доступны всем без аутентификации
- `docker pull ghcr.io/user/repo/image:latest` работает без login
- Удобны для open-source проектов

Как сделать образ публичным:
1. Перейти на GitHub → Packages
2. Выбрать образ → Settings
3. Danger Zone → Change visibility → Public

## Работа с Pull Request

### Что такое Pull Request (PR)?

**Pull Request** — запрос на включение изменений из одной ветки в другую. Используется для:
- Ревью кода перед merge
- Автоматического тестирования изменений (CI)
- Обсуждения реализации

### Типичный workflow с PR

1. **Создание ветки:**
   ```bash
   git checkout -b feature/my-feature
   git commit -am "Add feature"
   git push origin feature/my-feature
   ```

2. **Создание PR через GitHub UI:**
   - GitHub → Pull requests → New pull request
   - Выбрать базовую ветку (main) и ветку с изменениями
   - Добавить описание и создать PR

3. **Автоматические проверки:**
   - GitHub Actions запускает workflow
   - Выполняются тесты, сборка, линтеры
   - Статус отображается в PR

4. **Ревью и merge:**
   - Другие разработчики проверяют код
   - После одобрения — merge в базовую ветку
   - GitHub может автоматически удалить ветку

### CI проверки на PR

Типичная конфигурация для PR:
```yaml
on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm test
```

**Важно:** На PR обычно выполняются только проверки (build, test, lint), но НЕ публикация артефактов (deploy, push образов).

## Кэширование в GitHub Actions

**Кэширование** ускоряет workflow, сохраняя зависимости между запусками.

### Кэширование для Docker

GitHub предоставляет встроенное кэширование Docker layers через **GitHub Actions Cache (gha)**.

```yaml
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

Преимущества:
- Автоматическое управление кэшем
- Ускорение повторных сборок в 2-5 раз
- Не требует настройки

## Переменные и секреты

### Встроенные переменные

GitHub предоставляет полезные переменные:
- `${{ github.repository }}` — owner/repo (например, `user/myproject`)
- `${{ github.actor }}` — пользователь, запустивший workflow
- `${{ github.sha }}` — полный commit SHA
- `${{ github.ref }}` — ссылка на ветку/тег
- `${{ github.event_name }}` — тип события (push, pull_request)

### GITHUB_TOKEN

**GITHUB_TOKEN** — автоматически создаваемый секрет для аутентификации в GitHub API и ghcr.io.

Доступен через: `${{ secrets.GITHUB_TOKEN }}`

Используется для:
- Публикации в GitHub Container Registry
- Работы с GitHub API
- Создания комментариев в PR

Разрешения настраиваются в workflow:
```yaml
permissions:
  contents: read
  packages: write
```

## Best Practices

### 1. Используйте конкретные версии actions

❌ Плохо:
```yaml
- uses: actions/checkout@master
```

✅ Хорошо:
```yaml
- uses: actions/checkout@v4
```

### 2. Кэшируйте зависимости

Для npm:
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'
```

Для Docker:
```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

### 3. Используйте matrix для параллелизации

Вместо копирования job для каждого сервиса:
```yaml
strategy:
  matrix:
    service: [bot, api, frontend]
```

### 4. Разделяйте сборку и публикацию

На PR — только build:
```yaml
- name: Build image
  if: github.event_name == 'pull_request'
  run: docker build .
```

На push — build + push:
```yaml
- name: Build and push
  if: github.event_name == 'push'
  uses: docker/build-push-action@v5
  with:
    push: true
```

### 5. Давайте понятные имена

❌ Плохо:
```yaml
- name: Run
  run: npm test
```

✅ Хорошо:
```yaml
- name: Run unit tests
  run: npm test
```

## Примеры workflow

### Простой CI для тестирования

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install dependencies
        run: npm install
      - name: Run tests
        run: npm test
```

### Build и Push Docker образов

```yaml
name: Build and Push

on:
  push:
    branches: [main]

jobs:
  docker:
    runs-on: ubuntu-latest
    permissions:
      packages: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      
      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}/app:latest
```

### Matrix сборка для нескольких сервисов

```yaml
name: Build Services

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [bot, api, frontend]
    steps:
      - uses: actions/checkout@v4
      - name: Build ${{ matrix.service }}
        run: docker build -f Dockerfile.${{ matrix.service }} -t ${{ matrix.service }} .
```

## Полезные ссылки

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## Заключение

GitHub Actions — мощный инструмент для автоматизации CI/CD прямо в репозитории. Основные преимущества:

✅ Бесплатно для публичных репозиториев  
✅ Глубокая интеграция с GitHub  
✅ Встроенный Container Registry  
✅ Простой YAML синтаксис  
✅ Богатая экосистема готовых actions  

В следующих документах мы используем GitHub Actions для автоматической сборки и публикации Docker образов проекта.

