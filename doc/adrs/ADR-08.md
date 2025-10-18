# ADR-08: Docker-контейнеризация и лучшие практики

**Статус:** Принято  
**Дата:** 2025-10-17  
**Контекст:** Sprint D1 - Docker Images & Best Practices  
**Авторы:** DevOps Team

## Контекст и проблема

Проект systech-aidd-live состоит из трёх сервисов (Telegram Bot, FastAPI API, Next.js Frontend) и требует единообразного подхода к контейнеризации для:
- Локальной разработки с hot reload
- Production deployment с оптимизацией размера образов
- CI/CD автоматизации
- Безопасности и лучших практик

**Особенности проекта:**
- Плоская структура: Bot и API делят директорию `/src`
- Python-зависимости через UV (современный менеджер пакетов)
- Frontend на Next.js 15 с pnpm
- PostgreSQL 16 как БД

## Принятые решения

### 1. Multi-stage Builds

**Решение:** Использовать multi-stage builds для всех Dockerfile.

**Обоснование:**
- Разделение этапов сборки (builder) и runtime минимизирует размер итоговых образов
- Builder stage содержит компиляторы и dev-инструменты
- Runtime stage содержит только необходимые runtime-зависимости и артефакты
- Уменьшение attack surface для безопасности

**Реализация:**
- **Bot (Dockerfile.bot):** 2 stage - builder с UV, runtime с Python 3.11-slim
- **API (Dockerfile.api):** 2 stage - builder с UV, runtime с uvicorn
- **Frontend (Dockerfile.frontend):** 3 stage - deps, builder, runner

**Целевые размеры образов:**
- API: < 200 MB
- Frontend: < 150 MB  
- Bot: < 180 MB

### 2. Безопасность (Security Hardening)

**Решение:** Применить комплекс мер безопасности.

**Меры:**
1. **Non-root пользователи:**
   - Python services: `appuser` (UID 1001)
   - Frontend: `nextjs` (UID 1001) + `nodejs` group (GID 1001)
   
2. **Минимальные базовые образы:**
   - Python: `python:3.11-slim` (Debian-based, меньше Alpine для лучшей совместимости)
   - Node.js: `node:20-alpine` (минимальный Alpine для Node.js)

3. **Системные зависимости:**
   - Установка только необходимых пакетов (`--no-install-recommends`)
   - Очистка apt/apk cache после установки
   - Установка `ca-certificates` для HTTPS

4. **Read-only файловая система (где возможно):**
   - Writable только `/app/logs` директория
   - Остальное read-only для runtime

**Сканирование безопасности:**
- Hadolint для статического анализа Dockerfile
- Trivy для сканирования уязвимостей образов
- CI/CD интеграция для automated scanning

### 3. Кэширование слоёв Docker

**Решение:** Оптимизировать порядок команд для максимального кэширования.

**Стратегия:**
1. **Сначала зависимости, потом код:**
   ```dockerfile
   COPY pyproject.toml uv.lock ./
   RUN uv sync --frozen --no-dev
   COPY src/ /app/src/  # После установки зависимостей
   ```

2. **UV/pnpm lock files для детерминированности:**
   - `uv.lock` фиксирует версии Python-зависимостей
   - `pnpm-lock.yaml` фиксирует версии Node.js-зависимостей
   - `--frozen` флаги предотвращают неожиданные обновления

3. **Разделение редко и часто меняющихся слоёв:**
   - Системные зависимости (apt-get) - редко
   - Python/Node зависимости - средне
   - Исходный код - часто

**Результат:** При изменении кода пересобирается только последний слой (~5-10 сек).

### 4. Обработка плоской структуры проекта

**Проблема:** Bot (`src/main.py`) и API (`src/api/main.py`) используют общую директорию `/src`.

**Решение:**
- Build context для Bot и API: корень проекта (`.`)
- Dockerfile расположены в `devops/` для централизации
- В docker-compose.yml:
  ```yaml
  bot:
    build:
      context: ..          # Корень проекта
      dockerfile: devops/Dockerfile.bot
  ```

**Преимущества:**
- Нет дублирования кода между образами
- Единый source of truth для общих модулей
- Упрощённое обновление shared кода

### 5. Health Checks

**Решение:** Реализовать health checks для всех сервисов.

**Реализация:**

| Сервис | Health Check | Интервал | Timeout |
|--------|-------------|----------|---------|
| **Bot** | `pgrep -f "python -m src.main"` | 30s | 10s |
| **API** | `curl http://localhost:8000/health` | 30s | 10s |
| **Frontend** | `node -e "require('http').get(...)"` | 30s | 10s |
| **PostgreSQL** | `pg_isready -U systech_user` | 10s | 5s |

**Параметры:**
- `start_period`: Время на запуск (5-10s)
- `retries`: 3 попытки перед признанием unhealthy
- Используется в `depends_on` для правильного порядка запуска

### 6. Environment Variables & Configuration

**Решение:** Централизованное управление через `.env` файлы и environment variables.

**Структура:**
1. **`.env` (корень проекта):** Секреты и конфигурация для локальной разработки
   - `BOT_TOKEN`, `LLM_API_KEY`, `DATABASE_URL`
   
2. **docker-compose.yml:** Environment variables для контейнеров
   - Override `DATABASE_URL` для использования service name (`postgres:5432`)
   - Production-специфичные настройки (`UVICORN_WORKERS`)

3. **docker-compose.dev.yml:** Development overrides
   - `DATABASE_ECHO=true`, `LOG_LEVEL=DEBUG`
   - Hot reload настройки

**Best practices:**
- Секреты через `.env` (не коммитить в git)
- Defaults в Dockerfile через `ENV`
- Переопределение в compose файлах
- `.env.example` как документация

### 7. Оркестрация через Docker Compose

**Решение:** Два compose файла для разных сценариев.

**docker-compose.yml (Production):**
- Полная изоляция сервисов
- Build из Dockerfile без volume mounts
- Restart policies для отказоустойчивости
- Health checks и зависимости
- Expose только необходимых портов

**docker-compose.dev.yml (Development):**
- Volume mounts для hot reload:
  ```yaml
  volumes:
    - ../src:/app/src:ro      # Read-only для Python
    - ../frontend:/app:cached # Cached для Next.js
  ```
- Uvicorn с `--reload` флагом
- Next.js dev server (`pnpm dev`)
- Debug порты (5678 для debugpy)

**Использование:**
```bash
# Production
docker compose -f devops/docker-compose.yml up

# Development
docker compose -f devops/docker-compose.yml -f devops/docker-compose.dev.yml up
```

### 8. Next.js Standalone Output

**Решение:** Использовать Next.js standalone output для минимального образа.

**Конфигурация (next.config.ts):**
```typescript
const nextConfig: NextConfig = {
  output: 'standalone',
};
```

**Преимущества:**
- Автоматическое включение только необходимых зависимостей
- Размер образа уменьшается с ~800MB до ~150MB
- Self-contained сервер (`server.js`)
- Оптимальное для production deployment

**Структура в образе:**
```
/app/
  .next/standalone/       # Минимальный сервер
  .next/static/           # Статические ресурсы
  public/                 # Public assets
  server.js               # Entry point
```

### 9. UV для Python зависимостей

**Решение:** Использовать UV вместо pip для ускорения установки.

**Преимущества UV:**
- **Скорость:** 10-100x быстрее pip (Rust-based)
- **Детерминированность:** `uv.lock` для воспроизводимых сборок
- **Совместимость:** Работает с `pyproject.toml` (PEP 621)
- **Кэширование:** Встроенный кэш для повторных сборок

**Реализация:**
```dockerfile
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
RUN uv sync --frozen --no-dev
```

**Флаги:**
- `--frozen`: Не обновлять lock file (детерминированность)
- `--no-dev`: Исключить dev-зависимости для production

### 10. Размещение в папке `devops/`

**Решение:** Централизовать всю Docker-инфраструктуру в `devops/`.

**Структура:**
```
devops/
├── Dockerfile.bot           # Bot образ
├── Dockerfile.api           # API образ
├── Dockerfile.frontend      # Frontend образ
├── docker-compose.yml       # Production оркестрация
├── docker-compose.dev.yml   # Development overrides
├── .hadolint.yaml           # Hadolint конфигурация
└── doc/                     # DevOps документация
```

**Преимущества:**
- Чёткое разделение concerns (devops vs application code)
- Упрощённый CI/CD (всё в одной папке)
- Легко найти и обновить Docker-конфигурацию
- Следует индустриальным практикам (аналогично `.github/workflows/`, `.circleci/`)

## Адаптация для промышленного использования

### Переход к публичному Container Registry

При переходе от локальной разработки к production deployment в облаке потребуется использование публичного container registry (Docker Hub, GitHub Container Registry, AWS ECR, Google GCR, Azure ACR).

#### Что потребуется изменить:

**1. docker-compose.yml - замена build на image:**

```yaml
# ❌ Локальная сборка (разработка)
services:
  api:
    build:
      context: ..
      dockerfile: devops/Dockerfile.api

# ✅ Публичный registry (production)
services:
  api:
    image: ghcr.io/organization/systech-aidd-api:v1.0.0
```

**2. Добавление версионирования (Semantic Versioning):**

Теги образов для разных окружений:
- `latest` - последняя стабильная версия (для production)
- `stable` - проверенная стабильная версия
- `v1.0.0` - конкретная версия (semver)
- `v1.0.0-rc.1` - release candidate
- `develop` - latest development build (для staging)
- `feature-xyz` - feature branches (для testing)

**3. CI/CD Pipeline интеграция:**

Добавить этапы в GitHub Actions / GitLab CI / Jenkins:

```yaml
# Пример GitHub Actions
name: Build and Push Docker Images

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    steps:
      # 1. Login в registry
      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      # 2. Build образов
      - name: Build images
        run: |
          docker build -f devops/Dockerfile.api -t ghcr.io/org/systech-aidd-api:latest .
          docker build -f devops/Dockerfile.bot -t ghcr.io/org/systech-aidd-bot:latest .
          docker build -f devops/Dockerfile.frontend -t ghcr.io/org/systech-aidd-frontend:latest frontend/
      
      # 3. Tag с версией (для git tags)
      - name: Tag with version
        if: startsWith(github.ref, 'refs/tags/v')
        run: |
          VERSION=${GITHUB_REF#refs/tags/}
          docker tag ghcr.io/org/systech-aidd-api:latest ghcr.io/org/systech-aidd-api:$VERSION
      
      # 4. Push в registry
      - name: Push images
        run: |
          docker push ghcr.io/org/systech-aidd-api:latest
          docker push ghcr.io/org/systech-aidd-bot:latest
          docker push ghcr.io/org/systech-aidd-frontend:latest
      
      # 5. Security scanning
      - name: Run Trivy scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ghcr.io/org/systech-aidd-api:latest
          severity: 'CRITICAL,HIGH'
```

**4. Обновление .env.example:**

```bash
# Registry Configuration
REGISTRY_URL=ghcr.io/organization
IMAGE_TAG=latest

# Или конкретные версии для каждого сервиса
API_IMAGE=${REGISTRY_URL}/systech-aidd-api:${IMAGE_TAG}
BOT_IMAGE=${REGISTRY_URL}/systech-aidd-bot:${IMAGE_TAG}
FRONTEND_IMAGE=${REGISTRY_URL}/systech-aidd-frontend:${IMAGE_TAG}
```

**5. Secrets Management в production:**

Вместо `.env` файлов использовать:
- **Kubernetes:** Secrets и ConfigMaps
- **Docker Swarm:** Docker Secrets
- **AWS ECS:** Parameter Store / Secrets Manager
- **Azure:** Key Vault
- **GCP:** Secret Manager

Пример для Kubernetes:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: systech-aidd-secrets
type: Opaque
stringData:
  BOT_TOKEN: "xxx"
  LLM_API_KEY: "xxx"
  DATABASE_URL: "postgresql://..."
```

#### Что НЕ потребуется менять:

✅ **Dockerfile остаются без изменений:**
- `devops/Dockerfile.bot`
- `devops/Dockerfile.api`
- `devops/Dockerfile.frontend`

✅ **Структура приложения:**
- Исходный код в `src/`, `frontend/`
- Точки входа (entry points)
- Environment variables

✅ **Health checks:**
- Реализация health endpoints
- Health check команды в Dockerfile

✅ **Логика работы сервисов:**
- Бизнес-логика
- API endpoints
- База данных миграции

✅ **Security настройки:**
- Non-root пользователи
- Минимальные образы
- Security hardening

#### Дополнительные рекомендации для production:

**1. Automated Builds:**
- Триггер сборки при push в `main` и `tags`
- Автоматическое тегирование по git tags
- Parallel builds для ускорения CI/CD

**2. Image Signing (верификация подлинности):**
```bash
# Cosign (CNCF project)
cosign sign ghcr.io/org/systech-aidd-api:v1.0.0

# Docker Content Trust
export DOCKER_CONTENT_TRUST=1
docker push ghcr.io/org/systech-aidd-api:v1.0.0
```

**3. Vulnerability Scanning в CI:**
```yaml
# Trivy в GitHub Actions
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/org/systech-aidd-api:latest
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'

- name: Upload to GitHub Security
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: 'trivy-results.sarif'
```

**4. Rollback процедура:**
```bash
# Откат к предыдущей версии
docker compose -f devops/docker-compose.yml pull
docker compose -f devops/docker-compose.yml up -d

# Или через environment variable
IMAGE_TAG=v1.0.0 docker compose -f devops/docker-compose.yml up -d
```

**5. Мониторинг размеров образов:**
- Tracking размера образов в CI metrics
- Alerts при росте размера > 10%
- Dashboard с историей размеров

**Примеры registry:**

| Registry | Use Case | Pricing |
|----------|----------|---------|
| **GitHub Container Registry (ghcr.io)** | Open source, GitHub-hosted repos | Free для публичных, включено в GitHub Plans |
| **Docker Hub** | Общедоступные образы, широкое использование | Free tier: 1 private repo, Rate limits |
| **AWS ECR** | AWS-native, интеграция с ECS/EKS | Pay-per-use (~$0.10/GB/month) |
| **Google GCR** | GCP-native, интеграция с GKE | Pay-per-use (~$0.10/GB/month) |
| **Azure ACR** | Azure-native, интеграция с AKS | От $5/month (Basic) |

**Рекомендация:** Для open source проектов - GitHub Container Registry (ghcr.io), для enterprise - облачный registry провайдера (ECR/GCR/ACR).

## Альтернативы

### 1. Alpine vs Debian-slim для Python

**Рассмотрено:** `python:3.11-alpine` вместо `python:3.11-slim`

**Отклонено:**
- Alpine использует musl libc вместо glibc (проблемы совместимости)
- Многие Python wheels требуют компиляции на Alpine (медленнее)
- Размер выигрыш ~30MB не стоит потенциальных проблем
- Debian-slim более стабильный и широко используемый

### 2. Docker Compose v2 syntax vs v3

**Рассмотрено:** Использование новейшего Docker Compose syntax (без version)

**Решение:** Оставить `version: '3.8'` для обратной совместимости
- Работает с Docker Compose v1 и v2
- Широко документирован и протестирован
- Миграция на новый syntax при необходимости тривиальна

### 3. Единый Dockerfile vs раздельные

**Рассмотрено:** Один Dockerfile с `--target` для bot/api

**Отклонено:**
- Bot и API имеют разные требования (health checks, ports)
- Разделение упрощает понимание и поддержку
- Build context одинаковый, дублирование минимально

## Последствия

### Положительные

✅ **Размер образов:** Уменьшение на 60-70% благодаря multi-stage builds  
✅ **Скорость сборки:** UV ускоряет установку Python-зависимостей в 10-20x  
✅ **Безопасность:** Non-root, minimal images, automated scanning  
✅ **Кэширование:** Оптимальный порядок слоёв для быстрых пересборок  
✅ **Developer Experience:** Hot reload в dev режиме, простые команды make  
✅ **Production-ready:** Health checks, restart policies, secrets management  
✅ **CI/CD готовность:** Легко интегрировать в pipelines  

### Отрицательные

⚠️ **Сложность:** Больше файлов и конфигураций для поддержки  
⚠️ **Learning curve:** Разработчики должны понимать Docker Compose  
⚠️ **Зависимость от Docker:** Обязательное требование для запуска проекта  

### Риски и митигация

| Риск | Вероятность | Влияние | Митигация |
|------|-------------|---------|-----------|
| Проблемы с UV на разных платформах | Низкая | Средняя | Fallback на pip в документации |
| Конфликты портов в dev | Средняя | Низкая | Документация + configurable ports |
| Размер образов растёт со временем | Средняя | Средняя | Monitoring + регулярный review |
| Security vulnerabilities в base images | Средняя | Высокая | Automated Trivy scanning в CI |

## Метрики успеха

- [ ] Все образы собираются без ошибок
- [ ] Health checks работают для всех сервисов
- [ ] Dev режим поддерживает hot reload
- [ ] Размеры образов в пределах целевых значений
- [ ] Hadolint проверка проходит без критичных warnings
- [ ] Trivy не находит CRITICAL уязвимостей
- [ ] Build time < 5 минут для полной сборки
- [ ] Rebuild с изменением кода < 30 секунд

## Связанные документы

- [ADR-06: PostgreSQL + SQLAlchemy](ADR-06.md) - Архитектура базы данных
- [GUIDE-09: Docker Deployment](../guides/09-docker-deployment.md) - Руководство по использованию
- [DevOps Roadmap](../../devops/doc/devops-roadmap.md) - План DevOps спринтов
- [Hadolint Best Practices](https://github.com/hadolint/hadolint)
- [Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)

## История изменений

- **2025-10-17:** Первая версия (Sprint D1)

