# GUIDE-10: CI/CD Pipeline

**Статус:** ✅ Актуально  
**Версия:** 1.0  
**Дата:** 2025-10-17  
**Время прочтения:** ~40 минут

---

## 📋 Содержание

1. [Обзор](#обзор)
2. [Архитектура Pipeline](#архитектура-pipeline)
3. [Детали Jobs](#детали-jobs)
4. [Локальное воспроизведение CI](#локальное-воспроизведение-ci)
5. [Настройка GitHub](#настройка-github)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)
8. [FAQ](#faq)

---

## Обзор

### Что такое CI/CD Pipeline?

**CI (Continuous Integration)** - автоматическая проверка и сборка кода при каждом изменении:
- ✅ Lint и type checking
- ✅ Автоматические тесты
- ✅ Сборка Docker образов
- ✅ Security scanning

**CD (Continuous Deployment)** - автоматический деплой в production (Sprint D3):
- 🚀 Deployment на production сервер
- 🔄 Rolling updates
- 📊 Monitoring и rollback

### Наш CI Pipeline

```
┌──────────────┐     ┌──────────────┐
│ lint-backend │     │lint-frontend │
└──────┬───────┘     └──────┬───────┘
       │                    │
       └────────┬───────────┘
                │
         ┌──────▼───────┐
         │     test     │
         └──────┬───────┘
                │
         ┌──────▼──────────┐
         │  build-images   │ (Matrix: bot, api, frontend)
         └──────┬──────────┘
                │
         ┌──────▼──────────┐
         │ security-scan   │ (только main)
         └──────┬──────────┘
                │
         ┌──────▼──────────┐
         │    publish      │ (только main)
         └─────────────────┘
```

**Время выполнения:**
- PR (без main): ~4-5 минут
- Main push (полный): ~7-8 минут

### Triggers

Pipeline запускается автоматически при:

| Event | Branches | Jobs |
|-------|----------|------|
| **Push** | `main`, `develop` | Все jobs включая publish |
| **Pull Request** | `main`, `develop` | Lint, test, build (без publish) |

---

## Архитектура Pipeline

### Файл: `.github/workflows/ci.yml`

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

permissions:
  contents: read      # Чтение кода
  packages: write     # Публикация в ghcr.io

env:
  REGISTRY: ghcr.io
  IMAGE_PREFIX: ${{ github.repository }}
```

### Environment Variables

| Variable | Значение | Описание |
|----------|----------|----------|
| `REGISTRY` | `ghcr.io` | GitHub Container Registry |
| `IMAGE_PREFIX` | `owner/repo` | Префикс для имен образов |
| `GITHUB_TOKEN` | Auto | Автоматически предоставляется GitHub |

---

## Детали Jobs

### Job 1: lint-backend

**Назначение:** Проверка качества Python кода

**Шаги:**
1. Checkout кода
2. Установка UV package manager
3. Установка Python 3.11
4. Установка зависимостей через `uv sync`
5. Запуск Ruff lint (`ruff check`)
6. Проверка форматирования (`ruff format --check`)
7. Проверка типов MyPy (`mypy`)

**Используемые инструменты:**
- **Ruff** - быстрый линтер и форматтер (замена black, isort, flake8)
- **MyPy** - статическая проверка типов (strict mode)

**Локальный запуск:**
```bash
make ci-lint-backend

# Или напрямую:
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run mypy src/ tests/
```

**Типичные ошибки:**
```bash
# Ошибка: неиспользуемый импорт
src/main.py:5:1: F401 `sys` imported but unused

# Исправление:
uv run ruff check --fix src/

# Ошибка: неправильное форматирование
src/config.py: 1 file would be reformatted

# Исправление:
uv run ruff format src/

# Ошибка MyPy: отсутствует type hint
src/handler.py:10: error: Function is missing a return type annotation

# Исправление: добавить -> ReturnType
```

**Время выполнения:** ~40-60 секунд

---

### Job 2: lint-frontend

**Назначение:** Проверка качества TypeScript/Next.js кода

**Шаги:**
1. Checkout кода
2. Установка Node.js 20
3. Установка pnpm 8
4. Cache pnpm store для ускорения
5. Установка зависимостей (`pnpm install`)
6. ESLint проверка
7. TypeScript type check
8. Prettier format check

**Используемые инструменты:**
- **ESLint** - линтер для JavaScript/TypeScript
- **TypeScript** - проверка типов
- **Prettier** - проверка форматирования

**Локальный запуск:**
```bash
make ci-lint-frontend

# Или напрямую:
cd frontend
pnpm lint
pnpm type-check
pnpm format:check
```

**Типичные ошибки:**
```bash
# Ошибка ESLint: неиспользуемая переменная
error: 'React' is defined but never used  @typescript-eslint/no-unused-vars

# Исправление:
cd frontend && pnpm lint --fix

# Ошибка TypeScript: несовместимые типы
error TS2322: Type 'string' is not assignable to type 'number'

# Исправление: поправить типы в коде

# Ошибка Prettier: неправильное форматирование
[warn] frontend/app/page.tsx: Code style issues found

# Исправление:
cd frontend && pnpm format
```

**Время выполнения:** ~45-70 секунд (с кэшом pnpm)

---

### Job 3: test

**Назначение:** Запуск unit тестов с coverage

**Шаги:**
1. Checkout кода
2. Установка UV и Python 3.11
3. Установка зависимостей
4. Запуск pytest с coverage (без integration тестов)
5. Upload coverage report в Codecov (опционально)

**Команда pytest:**
```bash
uv run pytest -m "not integration" \
  --cov=src \
  --cov-report=xml \
  --cov-report=term
```

**Параметры:**
- `-m "not integration"` - пропускаем integration тесты (требуют LLM API)
- `--cov=src` - измеряем coverage только для src/
- `--cov-report=xml` - XML отчет для Codecov
- `--cov-report=term` - вывод в консоль

**Локальный запуск:**
```bash
make ci-test

# Или с coverage в HTML:
make test-cov
```

**Пример вывода:**
```
==================== test session starts ====================
collected 30 items

tests/test_config.py ......                          [ 20%]
tests/test_message.py ....                           [ 33%]
tests/test_command_handler.py ......                 [ 53%]
tests/test_llm_client.py ...                         [ 63%]
tests/test_context_manager.py ...                    [ 73%]
tests/test_message_handler.py .......                [100%]

---------- coverage: platform darwin, python 3.11.9 ----------
Name                       Stmts   Miss  Cover
----------------------------------------------
src/__init__.py               0      0   100%
src/config.py                42      0   100%
src/message.py               12      0   100%
...
----------------------------------------------
TOTAL                       165      0   100%

==================== 27 passed in 2.81s ====================
```

**Типичные ошибки:**
```bash
# Ошибка: упавший тест
FAILED tests/test_handler.py::test_handle_message - AssertionError

# Решение: посмотреть детали ошибки и исправить код

# Ошибка: низкий coverage
TOTAL coverage: 85% (target: 90%)

# Решение: добавить тесты для непокрытых строк
```

**Время выполнения:** ~30-45 секунд

---

### Job 4: build-images

**Назначение:** Сборка Docker образов для всех сервисов

**Strategy Matrix:**
```yaml
strategy:
  matrix:
    service: [bot, api, frontend]
```

Это создает 3 параллельных job для каждого сервиса.

**Шаги для каждого образа:**
1. Checkout кода
2. Setup Docker Buildx (BuildKit)
3. Извлечение metadata (tags, labels)
4. Сборка образа с layer caching
5. Сохранение образа как artifact

**Docker Build Parameters:**
```yaml
- uses: docker/build-push-action@v5
  with:
    context: .
    file: devops/Dockerfile.${{ matrix.service }}
    push: false  # Не пушим сразу, сохраняем artifact
    tags: ${{ steps.meta.outputs.tags }}
    labels: ${{ steps.meta.outputs.labels }}
    cache-from: type=gha,scope=${{ matrix.service }}
    cache-to: type=gha,mode=max,scope=${{ matrix.service }}
    outputs: type=docker,dest=/tmp/${{ matrix.service }}-image.tar
```

**Tagging Strategy:**

| Event | Tags |
|-------|------|
| PR | `sha-abc123`, `pr-42` |
| Main | `sha-abc123`, `branch-main`, `latest` |

**Layer Caching:**
- `cache-from: type=gha` - восстановление кэша из GitHub Actions cache
- `cache-to: type=gha,mode=max` - сохранение всех промежуточных слоев
- `scope=${{ matrix.service }}` - изолированный кэш для каждого сервиса

**Локальный запуск:**
```bash
make ci-build

# Или для конкретного сервиса:
docker build -f devops/Dockerfile.bot -t systech-aidd-bot:local .
docker build -f devops/Dockerfile.api -t systech-aidd-api:local .
docker build -f devops/Dockerfile.frontend -t systech-aidd-frontend:local .
```

**Оптимизации:**
1. **BuildKit** - быстрее классического Docker build
2. **Layer caching** - переиспользование слоев между сборками
3. **Matrix parallelization** - 3 сервиса собираются одновременно
4. **Multi-stage builds** - минимальный размер финальных образов

**Время выполнения:**
- Первая сборка (cold cache): ~5-7 минут
- Повторная сборка (warm cache): ~2-3 минуты

**Размеры образов:**
- Bot: ~180 MB
- API: ~200 MB  
- Frontend: ~150 MB

---

### Job 5: security-scan

**Назначение:** Сканирование уязвимостей в Docker образах

**Условие запуска:** Только на `main` ветке
```yaml
if: github.ref == 'refs/heads/main'
```

**Strategy Matrix:** Сканирует все 3 сервиса параллельно

**Шаги:**
1. Download образа из artifacts (предыдущий job)
2. Load образа в Docker
3. Запуск Trivy vulnerability scanner
4. Генерация SARIF отчета
5. Upload отчета в GitHub Security tab

**Trivy Configuration:**
```yaml
- uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/owner/repo-service:sha-${{ github.sha }}
    format: 'sarif'
    output: 'trivy-results-${{ matrix.service }}.sarif'
    severity: 'HIGH,CRITICAL'
```

**Что сканирует Trivy:**
- ✅ OS packages (apt, apk, yum)
- ✅ Application dependencies (npm, pip, etc.)
- ✅ Embedded secrets
- ✅ IaC misconfigurations

**Просмотр результатов:**
1. GitHub → Security tab
2. Vulnerability alerts
3. Code scanning alerts

**Локальный запуск:**
```bash
# Установка Trivy
brew install trivy  # macOS
# или
docker pull aquasec/trivy

# Сканирование образа
trivy image systech-aidd-bot:local

# Только HIGH и CRITICAL
trivy image --severity HIGH,CRITICAL systech-aidd-api:local
```

**Пример вывода:**
```
systech-aidd-bot:local (alpine 3.18.4)
======================================
Total: 5 (HIGH: 3, CRITICAL: 2)

┌────────────┬────────────────┬──────────┬──────────┬───────────────┐
│  Library   │ Vulnerability  │ Severity │ Installed│   Fixed In    │
├────────────┼────────────────┼──────────┼──────────┼───────────────┤
│ openssl    │ CVE-2023-12345 │ CRITICAL │ 3.0.10   │ 3.0.11        │
│ libcurl    │ CVE-2023-67890 │ HIGH     │ 8.1.0    │ 8.1.2         │
└────────────┴────────────────┴──────────┴──────────┴───────────────┘
```

**Исправление уязвимостей:**
1. Обновить base image в Dockerfile
2. Обновить зависимости (package.json, pyproject.toml)
3. Пересобрать образ

**Время выполнения:** ~1-2 минуты на образ

---

### Job 6: publish

**Назначение:** Публикация образов в GitHub Container Registry

**Условия запуска:**
- Только на `main` ветке
- После успешного build и security scan

**Strategy Matrix:** Публикует все 3 сервиса параллельно

**Шаги:**
1. Download образа из artifacts
2. Load образа в Docker
3. Login в ghcr.io через `GITHUB_TOKEN`
4. Extract metadata для tags
5. Tag образа
6. Push всех тегов в registry

**Tagging для main:**
```
ghcr.io/owner/repo-bot:sha-abc123
ghcr.io/owner/repo-bot:branch-main
ghcr.io/owner/repo-bot:latest
```

**Локальный эквивалент:**
```bash
# Login (нужен Personal Access Token)
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Tag
docker tag systech-aidd-bot:local ghcr.io/owner/repo-bot:latest

# Push
docker push ghcr.io/owner/repo-bot:latest
```

**Просмотр опубликованных образов:**
1. GitHub → Packages
2. Выбрать образ (bot/api/frontend)
3. Видны все tags, размеры, даты публикации

**Pull образа:**
```bash
# Публичный образ
docker pull ghcr.io/owner/repo-bot:latest

# Приватный образ (требуется authentication)
docker login ghcr.io
docker pull ghcr.io/owner/repo-bot:latest
```

**Время выполнения:** ~2-3 минуты на образ

---

## Локальное воспроизведение CI

### Зачем запускать CI локально?

1. ✅ **Быстрая обратная связь** - не ждать GitHub Actions
2. ✅ **Экономия CI minutes** - особенно для приватных репозиториев
3. ✅ **Отладка** - легче разобраться в проблемах локально
4. ✅ **Pre-commit проверки** - убедиться что код пройдет CI

### Makefile команды

Добавлены специальные команды для воспроизведения CI локально:

```bash
# Backend lint (как в CI)
make ci-lint-backend

# Frontend lint (как в CI)
make ci-lint-frontend

# Tests (как в CI)
make ci-test

# Build образов (как в CI)
make ci-build

# Полная CI проверка
make ci-check-all
```

### Детальные команды

#### Backend Lint
```bash
make ci-lint-backend

# Что выполняется:
# 1. uv run ruff check src/ tests/
# 2. uv run ruff format --check src/ tests/
# 3. uv run mypy src/ tests/
```

**Автоисправление:**
```bash
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/
```

#### Frontend Lint
```bash
make ci-lint-frontend

# Что выполняется:
# 1. cd frontend && pnpm lint
# 2. cd frontend && pnpm type-check
# 3. cd frontend && pnpm format:check
```

**Автоисправление:**
```bash
cd frontend
pnpm lint --fix
pnpm format
```

#### Tests
```bash
make ci-test

# Выполняется:
# uv run pytest -m "not integration" --cov=src --cov-report=term
```

**С HTML coverage отчетом:**
```bash
make test-cov
open htmlcov/index.html  # macOS
```

#### Build Images
```bash
make ci-build

# Выполняется параллельно (если система поддерживает):
# docker build -f devops/Dockerfile.bot -t systech-aidd-bot:local .
# docker build -f devops/Dockerfile.api -t systech-aidd-api:local .
# docker build -f devops/Dockerfile.frontend -t systech-aidd-frontend:local .
```

**Проверка собранных образов:**
```bash
docker images | grep systech-aidd

# Запуск для тестирования:
docker run --rm systech-aidd-bot:local --version
```

#### Полная проверка
```bash
make ci-check-all

# Выполняет последовательно:
# 1. ci-lint-backend
# 2. ci-lint-frontend
# 3. ci-test
# 4. ci-build
```

**Время выполнения:** ~8-10 минут (первый раз), ~3-5 минут (с кэшом)

---

## Настройка GitHub

### Шаг 1: GitHub Actions Permissions

**Путь:** `Settings` → `Actions` → `General` → `Workflow permissions`

**Настройка:**
1. Выбрать: **Read and write permissions**
2. Отметить: **Allow GitHub Actions to create and approve pull requests** (опционально)

**Почему нужно:**
- Pipeline должен публиковать образы в GitHub Container Registry
- `GITHUB_TOKEN` с write permissions для packages

**Скриншот локации:**
```
Repository → Settings → Actions → General
   └─ Workflow permissions
      ☑ Read and write permissions
      ☐ Read repository contents and packages permissions
```

### Шаг 2: Branch Protection (рекомендуется)

**Путь:** `Settings` → `Branches` → `Add branch protection rule`

**Правила для `main`:**
```yaml
Branch name pattern: main

☑ Require status checks to pass before merging
  ☑ Require branches to be up to date before merging
  Status checks:
    ☑ lint-backend
    ☑ lint-frontend  
    ☑ test
    ☑ build-images

☑ Require conversation resolution before merging

☐ Require signed commits (опционально)
☐ Require linear history (опционально)
```

**Эффект:**
- Нельзя merge PR с failing CI
- Гарантируется качество кода в main

### Шаг 3: Публичность образов

**По умолчанию:** Образы создаются как **private**

**Сделать образы публичными:**

1. После первой публикации перейти: GitHub → Packages
2. Выбрать образ (например, `systech-aidd-bot`)
3. `Package settings` → `Change visibility`
4. Выбрать `Public`
5. Подтвердить изменение (ввести имя образа)

**Когда использовать:**
- ✅ Public - для open-source проектов
- ❌ Private - для корпоративных/коммерческих проектов

### Шаг 4: Secrets (будущее)

Для текущего Sprint D2 дополнительные secrets **не требуются**.

**В будущем (Sprint D3 - CD):**

```bash
Settings → Secrets and variables → Actions → New repository secret
```

**Примеры secrets:**
- `DEPLOY_SSH_KEY` - для SSH deployment
- `SLACK_WEBHOOK` - для notifications
- `DOCKER_HUB_TOKEN` - если используется Docker Hub
- `CODECOV_TOKEN` - для Codecov integration

### Шаг 5: Проверка настроек

**После настройки:**

1. Создать тестовую ветку:
   ```bash
   git checkout -b test-ci
   echo "# Test" >> README.md
   git add README.md
   git commit -m "test: CI pipeline"
   git push -u origin test-ci
   ```

2. Открыть PR в GitHub

3. Проверить что workflow запустился:
   - GitHub → Actions tab
   - Видеть запущенный workflow
   - Все jobs должны выполниться успешно

4. Merge PR в main (если всё OK)

5. Проверить что образы опубликовались:
   - GitHub → Packages
   - Видеть 3 образа (bot, api, frontend)
   - С тегами `latest`, `branch-main`, `sha-...`

---

## Troubleshooting

### Проблема: Workflow не запускается

**Симптомы:**
- Push в ветку, но workflow не появляется в Actions tab

**Причины и решения:**

1. **Неправильный branch в triggers**
   ```yaml
   # Проверить в .github/workflows/ci.yml:
   on:
     push:
       branches: [main, develop]  # Ваша ветка должна быть в списке
   ```

2. **Синтаксическая ошибка в YAML**
   ```bash
   # Проверить YAML онлайн:
   # https://www.yamllint.com/
   
   # Или локально:
   yamllint .github/workflows/ci.yml
   ```

3. **Actions отключены в репозитории**
   ```
   Settings → Actions → General
   ☑ Allow all actions and reusable workflows
   ```

### Проблема: lint-backend fails

**Симптомы:**
```
Error: Process completed with exit code 1
```

**Решения:**

1. **Запустить локально:**
   ```bash
   make ci-lint-backend
   ```

2. **Посмотреть детали ошибки:**
   ```bash
   uv run ruff check src/ tests/
   # Исправить показанные ошибки
   
   uv run mypy src/ tests/
   # Добавить type hints где необходимо
   ```

3. **Автоисправление:**
   ```bash
   uv run ruff check --fix src/ tests/
   uv run ruff format src/ tests/
   ```

### Проблема: lint-frontend fails

**Решения:**

1. **Запустить локально:**
   ```bash
   cd frontend
   pnpm lint
   pnpm type-check
   ```

2. **Автоисправление:**
   ```bash
   cd frontend
   pnpm lint --fix
   pnpm format
   ```

3. **Проверить node_modules:**
   ```bash
   cd frontend
   rm -rf node_modules pnpm-lock.yaml
   pnpm install
   ```

### Проблема: test fails

**Симптомы:**
```
FAILED tests/test_handler.py::test_handle_message - AssertionError
```

**Решения:**

1. **Запустить локально:**
   ```bash
   make ci-test
   ```

2. **Запустить конкретный тест:**
   ```bash
   uv run pytest tests/test_handler.py::test_handle_message -v
   ```

3. **Запустить с отладкой:**
   ```bash
   uv run pytest tests/test_handler.py::test_handle_message -v -s --pdb
   ```

4. **Проверить fixtures:**
   - Убедиться что моки настроены правильно
   - Проверить conftest.py

### Проблема: build-images timeout или fails

**Симптомы:**
```
Error: buildx failed with: ERROR: failed to solve: process timeout
```

**Решения:**

1. **Проверить Dockerfile:**
   ```bash
   docker build -f devops/Dockerfile.bot -t test .
   ```

2. **Проверить .dockerignore:**
   - Убедиться что большие файлы/директории исключены
   - node_modules, .git, htmlcov, etc.

3. **Увеличить timeout (в workflow):**
   ```yaml
   - name: Build Docker image
     timeout-minutes: 20  # Увеличить с 10 до 20
   ```

4. **Очистить кэш:**
   ```
   GitHub → Actions → Caches → Delete cache
   ```

### Проблема: security-scan находит критичные уязвимости

**Решения:**

1. **Просмотреть отчет:**
   ```
   GitHub → Security → Code scanning
   ```

2. **Обновить base image:**
   ```dockerfile
   # В Dockerfile обновить версию
   FROM python:3.11-slim  # текущая версия
   FROM python:3.11.8-slim  # конкретная версия
   ```

3. **Обновить зависимости:**
   ```bash
   # Backend
   uv lock --upgrade
   
   # Frontend
   cd frontend && pnpm update
   ```

4. **Временно игнорировать (не рекомендуется):**
   ```yaml
   # В trivy-action добавить:
   ignore-unfixed: true
   ```

### Проблема: publish fails - authentication

**Симптомы:**
```
Error: denied: permission_denied
```

**Решения:**

1. **Проверить permissions в workflow:**
   ```yaml
   permissions:
     contents: read
     packages: write  # Должно быть!
   ```

2. **Проверить Settings:**
   ```
   Settings → Actions → General → Workflow permissions
   ☑ Read and write permissions
   ```

3. **Проверить что push только на main:**
   ```yaml
   if: github.ref == 'refs/heads/main'
   ```

### Проблема: Образы не видны в Packages

**Решения:**

1. **Проверить что workflow выполнился на main:**
   - publish job запускается только на main

2. **Проверить логи publish job:**
   ```
   Actions → выбрать workflow run → publish
   ```

3. **Проверить имя репозитория:**
   - Образы публикуются с именем `ghcr.io/owner/repo-service`

4. **Подождать несколько минут:**
   - GitHub может обрабатывать образы с задержкой

---

## Best Practices

### Разработка

1. **Запускать CI локально перед push:**
   ```bash
   make ci-check-all
   ```

2. **Делать небольшие commits:**
   - Легче найти причину ошибки в CI
   - Быстрее проходят CI checks

3. **Использовать feature branches:**
   ```bash
   git checkout -b feature/new-feature
   # Разработка
   git push -u origin feature/new-feature
   # Создать PR
   ```

4. **Следить за coverage:**
   - Поддерживать coverage > 80%
   - Добавлять тесты для нового кода

### CI/CD

1. **Не коммитить в main напрямую:**
   - Использовать PR workflow
   - Обязательный code review

2. **Мониторить failed builds:**
   - GitHub → Actions → Failed workflows
   - Исправлять сразу

3. **Оптимизировать время выполнения:**
   - Использовать caching
   - Параллелизация где возможно
   - Избегать тяжелых операций в CI

4. **Документировать изменения в CI:**
   - Обновлять этот guide при изменениях
   - Добавлять комментарии в workflow файл

### Docker

1. **Оптимизировать образы:**
   - Multi-stage builds
   - Минимальные base images
   - .dockerignore актуален

2. **Использовать конкретные версии:**
   ```dockerfile
   # Плохо
   FROM node:20
   
   # Хорошо
   FROM node:20.10.0-alpine
   ```

3. **Тестировать образы локально:**
   ```bash
   make ci-build
   docker run --rm systech-aidd-bot:local
   ```

### Security

1. **Регулярно обновлять зависимости:**
   ```bash
   # Backend
   uv lock --upgrade
   
   # Frontend
   cd frontend && pnpm update
   ```

2. **Мониторить security alerts:**
   - GitHub → Security → Dependabot alerts
   - Исправлять ASAP

3. **Не хранить secrets в коде:**
   - Использовать GitHub Secrets
   - Проверять с помощью git-secrets

4. **Следить за Trivy отчетами:**
   - GitHub → Security → Code scanning

---

## FAQ

### Q: Сколько стоит запуск CI?

**A:** Для публичных репозиториев - **бесплатно** (unlimited)

Для приватных:
- Free: 2,000 minutes/месяц
- Pro: 3,000 minutes/месяц  
- Team: 3,000 minutes/месяц

Наш pipeline: ~7 минут на запуск
- ~40 запусков в месяц при активной разработке
- ~280 minutes/месяц - **в пределах free tier**

### Q: Можно ли пропустить CI для некоторых коммитов?

**A:** Да, добавить `[skip ci]` или `[ci skip]` в commit message:

```bash
git commit -m "docs: update README [skip ci]"
```

**Когда использовать:**
- Изменения только в документации (*.md)
- Изменения в .github кроме workflows

### Q: Как ускорить CI?

**A:** Несколько способов:

1. **Оптимизировать Docker builds:**
   - Улучшить .dockerignore
   - Порядок команд в Dockerfile (чаще меняющееся - ниже)

2. **Использовать caching эффективно:**
   - pnpm cache уже настроен
   - Docker layer cache уже настроен

3. **Запускать меньше jobs на PR:**
   - security-scan только на main (уже сделано)
   - publish только на main (уже сделано)

4. **Self-hosted runners:**
   - Для очень активных проектов
   - Требует настройки инфраструктуры

### Q: Что делать если CI часто падает?

**A:** Диагностика:

1. **Flaky tests:**
   ```bash
   # Запустить тест много раз
   for i in {1..10}; do make test; done
   ```
   - Исправить недетерминированное поведение
   - Улучшить изоляцию тестов

2. **Network issues:**
   - Добавить retry механизмы
   - Использовать mirrors для dependencies

3. **Timeout issues:**
   - Увеличить timeout
   - Оптимизировать медленные операции

### Q: Как добавить новый job в pipeline?

**A:** Пример добавления E2E тестов:

```yaml
# В .github/workflows/ci.yml добавить:

e2e-tests:
  name: E2E Tests
  runs-on: ubuntu-latest
  needs: [build-images]
  
  steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: "20"
    
    - name: Install Playwright
      run: cd frontend && npx playwright install
    
    - name: Run E2E tests
      run: cd frontend && pnpm test:e2e
```

### Q: Можно ли использовать другой registry вместо ghcr.io?

**A:** Да, легко. Пример для Docker Hub:

```yaml
# В ci.yml заменить:
env:
  REGISTRY: docker.io
  IMAGE_PREFIX: your-dockerhub-username

# И добавить login step:
- name: Log in to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

См. [ADR-09](../adrs/ADR-09.md) для сравнения registries.

### Q: Как добавить notifications при failures?

**A:** Пример Slack notification:

```yaml
# Добавить в конец workflow:
notify-failure:
  name: Notify on Failure
  runs-on: ubuntu-latest
  needs: [lint-backend, lint-frontend, test, build-images]
  if: failure()
  
  steps:
    - name: Send Slack notification
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## Ссылки

**Документация проекта:**
- [ADR-08: Docker Best Practices](../adrs/ADR-08.md)
- [ADR-09: CI/CD Architecture](../adrs/ADR-09.md)
- [GUIDE-09: Docker Deployment](09-docker-deployment.md)
- [DevOps Roadmap](../../devops/doc/devops-roadmap.md)

**External:**
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)

**Инструменты:**
- [Ruff](https://docs.astral.sh/ruff/)
- [MyPy](https://mypy.readthedocs.io/)
- [ESLint](https://eslint.org/)
- [Pytest](https://docs.pytest.org/)

---

## Changelog

| Дата | Версия | Изменения |
|------|--------|-----------|
| 2025-10-17 | 1.0 | Первая версия guide по CI/CD |

---

**Следующий шаг:** [Sprint D3 - CD Pipeline & Deployment](../../devops/doc/devops-roadmap.md#sprint-d3-cd-pipeline--deployment)

