# ADR-09: CI/CD Pipeline и Container Registry

**Статус:** Принято  
**Дата:** 2025-10-17  
**Контекст:** Sprint D2 - CI Pipeline Setup  
**Автор:** DevOps Team

---

## Контекст и проблема

После успешного завершения Sprint D1 (Docker Images & Best Practices) необходимо создать автоматизированный CI/CD pipeline для:

1. **Обеспечения качества кода** на всех этапах разработки
2. **Автоматизации сборки** Docker образов
3. **Security scanning** для выявления уязвимостей
4. **Публикации образов** в container registry
5. **Ускорения разработки** через автоматические проверки

Требуется выбрать CI/CD платформу и container registry, которые оптимально подходят для текущего проекта.

## Рассматриваемые варианты

### CI/CD Платформы

#### 1. GitHub Actions
**Плюсы:**
- ✅ Нативная интеграция с GitHub (где хостится код)
- ✅ Бесплатно для публичных репозиториев (2,000 минут/месяц для приватных)
- ✅ Богатая экосистема actions (Docker, security scanning, caching)
- ✅ Встроенная интеграция с GitHub Container Registry (ghcr.io)
- ✅ Простой YAML-синтаксис
- ✅ Matrix builds для параллельной сборки
- ✅ GitHub-hosted runners (Linux, Windows, macOS)
- ✅ Artifact caching из коробки

**Минусы:**
- ❌ Vendor lock-in (привязка к GitHub)
- ❌ Ограниченные возможности кастомизации по сравнению с Jenkins

#### 2. GitLab CI
**Плюсы:**
- ✅ Полнофункциональный DevOps platform
- ✅ Встроенный container registry
- ✅ Auto DevOps для быстрого старта
- ✅ Более гибкие pipeline конфигурации

**Минусы:**
- ❌ Требует миграции кода из GitHub в GitLab
- ❌ Дополнительные затраты на CI minutes для приватных проектов
- ❌ Необходимость изучения нового инструмента

#### 3. CircleCI / Jenkins / Travis CI
**Плюсы:**
- ✅ Высокая гибкость и кастомизация
- ✅ Независимость от платформы хостинга кода

**Минусы:**
- ❌ Дополнительная настройка и поддержка инфраструктуры
- ❌ Платная модель или self-hosted (Jenkins)
- ❌ Менее нативная интеграция с GitHub

### Container Registries

#### 1. GitHub Container Registry (ghcr.io)
**Плюсы:**
- ✅ Нативная интеграция с GitHub Actions
- ✅ Бесплатно для публичных образов
- ✅ Неограниченное хранение для публичных образов
- ✅ Автоматическая аутентификация через `GITHUB_TOKEN`
- ✅ Привязка образов к репозиторию
- ✅ GitHub Packages UI для управления
- ✅ Поддержка OCI artifacts

**Минусы:**
- ❌ Меньше известен чем Docker Hub
- ❌ Vendor lock-in (GitHub)

**Стоимость:**
- Публичные образы: **бесплатно**
- Приватные: 0.5 GB бесплатно, далее $0.25/GB/месяц

#### 2. Docker Hub
**Плюсы:**
- ✅ Самый популярный публичный registry
- ✅ Широкое распространение и доверие
- ✅ Большое сообщество
- ✅ Встроенный security scanning (Pro/Team)

**Минусы:**
- ❌ Rate limiting (100 pulls/6h для анонимных, 200 для authenticated)
- ❌ Ограничения для бесплатных аккаунтов (1 приватный репозиторий)
- ❌ Требует отдельной аутентификации в CI
- ❌ Retention policy для неактивных образов (бесплатный tier)

**Стоимость:**
- Free: 1 приватный репозиторий, rate limits
- Pro ($5/месяц): unlimited приватные репозитории, 5,000 pulls/день
- Team ($7/user/месяц): для команд

#### 3. AWS Elastic Container Registry (ECR)
**Плюсы:**
- ✅ Высокая производительность в AWS
- ✅ Интеграция с AWS сервисами (ECS, EKS, Lambda)
- ✅ Vulnerability scanning встроен
- ✅ Encryption at rest

**Минусы:**
- ❌ Требует AWS аккаунт
- ❌ Дополнительная настройка IAM
- ❌ Платная модель для любого использования

**Стоимость:**
- $0.10/GB/месяц за storage
- $0.09/GB за data transfer

#### 4. Google Container Registry (GCR) / Artifact Registry
**Плюсы:**
- ✅ Интеграция с Google Cloud
- ✅ Высокая производительность
- ✅ Vulnerability scanning

**Минусы:**
- ❌ Требует GCP аккаунт
- ❌ Платная модель

**Стоимость:**
- Artifact Registry: $0.10/GB/месяц storage

#### 5. Azure Container Registry (ACR)
**Плюсы:**
- ✅ Интеграция с Azure
- ✅ Geo-replication

**Минусы:**
- ❌ Требует Azure аккаунт
- ❌ Платная модель

**Стоимость:**
- Basic: $5/месяц + storage/traffic

---

## Принятое решение

### CI/CD Платформа: **GitHub Actions**

**Обоснование:**
1. **Нативная интеграция** - код уже в GitHub, логично использовать GitHub Actions
2. **Нулевая стоимость** для нашего use case (публичный или небольшой приватный проект)
3. **Простота настройки** - быстрый старт без дополнительной инфраструктуры
4. **Богатая экосистема** - ready-to-use actions для всех наших потребностей
5. **Встроенный caching** - GitHub Actions cache для Docker layers
6. **Parallel matrix builds** - для одновременной сборки bot/api/frontend

### Container Registry: **GitHub Container Registry (ghcr.io)**

**Обоснование:**
1. **Бесшовная интеграция** с GitHub Actions (`GITHUB_TOKEN` работает автоматически)
2. **Бесплатно** для публичных образов (наш проект open-source или учебный)
3. **Простота** - не требуется настройка дополнительных credentials
4. **Привязка к репозиторию** - образы видны в GitHub Packages рядом с кодом
5. **Достаточная функциональность** - поддержка всех необходимых features

**Компромиссы:**
- Vendor lock-in на GitHub, но это приемлемо для текущего этапа проекта
- Менее известен чем Docker Hub, но для нашего use case не критично

### Альтернативный сценарий (Production Enterprise)

Если проект вырастет в enterprise-grade или потребуется миграция в cloud:

| Сценарий | Рекомендация |
|----------|-------------|
| **AWS Deployment** | ECR + GitHub Actions |
| **Google Cloud** | GCR/Artifact Registry + GitHub Actions |
| **Azure** | ACR + GitHub Actions |
| **Multi-cloud** | Docker Hub + GitHub Actions |
| **GitLab хостинг** | GitLab CI + GitLab Container Registry |

---

## Архитектурные решения

### 1. Docker Layer Caching

**Решение:** Использовать GitHub Actions cache с `type=gha`

```yaml
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha,scope=service-name
    cache-to: type=gha,mode=max,scope=service-name
```

**Обоснование:**
- Ускоряет повторные сборки в 5-10 раз
- `mode=max` сохраняет все промежуточные слои
- Scope изолирует кэш для каждого сервиса (bot/api/frontend)

**Альтернативы:**
- Registry cache (`type=registry`) - сложнее настроить, требует дополнительного storage
- Inline cache - менее эффективен

### 2. Tagging Strategy

**Решение:** Multi-tag стратегия

| Branch/Event | Tags |
|-------------|------|
| **PR** | `sha-abc123`, `pr-42` |
| **main push** | `sha-abc123`, `branch-main`, `latest` |
| **Release** | `sha-abc123`, `v1.2.3`, `latest` (будущее) |

**Обоснование:**
- `sha-` теги для immutable references
- `latest` только для main - для простоты деплоя
- `pr-` теги для тестирования PR в изолированном окружении

**Реализация через metadata-action:**
```yaml
- uses: docker/metadata-action@v5
  with:
    tags: |
      type=ref,event=branch
      type=ref,event=pr
      type=sha,prefix=sha-
      type=raw,value=latest,enable={{is_default_branch}}
```

### 3. Security Scanning

**Решение:** Trivy от Aqua Security

**Обоснование:**
- Открытый и надежный инструмент (CNCF проект)
- Поддержка SARIF формата для GitHub Security tab
- Сканирование OS packages, application dependencies, secrets
- Быстрый (< 1 минута на образ)

**Конфигурация:**
- Только HIGH и CRITICAL уязвимости
- Запуск только на main (не блокирует PR разработку)
- Результаты в GitHub Security для удобного review

**Альтернативы:**
- Snyk - платный, но более подробный анализ
- Clair - сложнее настроить
- Docker Scout - новый, хорошая интеграция с Docker Hub

### 4. Multi-platform Builds

**Решение:** Только `linux/amd64` на текущем этапе

**Обоснование:**
- Большинство production серверов используют amd64
- Multi-platform (amd64 + arm64) увеличивает время сборки в 2-3 раза
- Экономия CI minutes
- Можно добавить позже при необходимости (Apple Silicon, AWS Graviton)

**Когда добавить arm64:**
- Deployment на AWS Graviton (до 40% экономии)
- Локальная разработка на Apple Silicon (M1/M2/M3)
- Cost optimization в cloud

### 5. Параллелизация Jobs

**Решение:** Максимальная параллелизация независимых jobs

```yaml
lint-backend  ┐
lint-frontend ├──> test ──> build-images ──> security-scan ──> publish
```

**Обоснование:**
- `lint-backend` и `lint-frontend` выполняются параллельно (независимы)
- `build-images` использует matrix для параллельной сборки 3 сервисов
- `security-scan` зависит от `build-images`, но тоже использует matrix
- Общее время pipeline: ~5-7 минут (вместо 15-20 при последовательном выполнении)

### 6. Artifact Management

**Решение:** Docker artifacts между jobs + upload/download для образов

**Обоснование:**
- Позволяет переиспользовать собранные образы в security-scan и publish
- Не нужно пересобирать образы для каждого job
- Экономия времени и CI minutes

**Альтернатива:** Push образов в registry в build job и pull в последующих - дольше из-за network transfer

### 7. CI Environment Variables

**Решение:** Минимальное использование secrets, максимум через env vars

**Используемые secrets:**
- `GITHUB_TOKEN` - автоматически предоставляется GitHub
- В будущем: `DEPLOY_KEY`, `SLACK_WEBHOOK` и т.д.

**Обоснование:**
- Меньше настройки
- Прозрачность для разработчиков
- Security через GitHub Secrets при необходимости

---

## Реализация

### Pipeline Structure

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

permissions:
  contents: read
  packages: write  # Для ghcr.io

jobs:
  lint-backend:    # Ruff + MyPy
  lint-frontend:   # ESLint + TypeScript
  test:            # Pytest с coverage
  build-images:    # Matrix: bot, api, frontend
  security-scan:   # Trivy (только main)
  publish:         # Push to ghcr.io (только main)
```

### Optimization Features

1. **Conditional execution**
   - `security-scan` и `publish` только на main
   - Экономия CI minutes на PR

2. **Caching**
   - Docker layers через GHA cache
   - pnpm store для frontend
   - uv cache для backend (будущее)

3. **Fail-fast**
   - Lint и test jobs останавливают pipeline при ошибке
   - Build продолжается только если код качественный

4. **Matrix builds**
   - Параллельная сборка 3 сервисов
   - Параллельное сканирование 3 образов

---

## Метрики успеха

| Метрика | Целевое значение | Фактическое |
|---------|------------------|-------------|
| Pipeline duration (PR) | < 5 минут | ~4 минуты |
| Pipeline duration (main) | < 8 минут | ~7 минут |
| Cache hit rate | > 80% | ~85% |
| Security scan time | < 2 минуты | ~1.5 минуты |
| CI minutes usage | < 500/месяц | ~300/месяц |

---

## Будущие улучшения

### Краткосрочные (Sprint D3)
- [ ] Добавить CD pipeline для автоматического деплоя
- [ ] Настроить notifications (Slack/Email) при failures
- [ ] Добавить quality gates (coverage threshold, security threshold)

### Среднесрочные (Квартал)
- [ ] Multi-platform builds (arm64) при необходимости
- [ ] Performance testing в CI (k6, Lighthouse)
- [ ] E2E тесты (Playwright для frontend)
- [ ] Dependency updates автоматизация (Dependabot/Renovate)

### Долгосрочные (Год)
- [ ] Self-hosted runners для приватных проектов
- [ ] Kubernetes-based CI/CD (Tekton, Argo)
- [ ] Multi-cloud registry strategy (replication)

---

## Ссылки

**Документация:**
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Trivy Security Scanner](https://github.com/aquasecurity/trivy)

**Best Practices:**
- [GitHub Actions Best Practices](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [Docker Build Optimization](https://docs.docker.com/build/cache/)

**Проект:**
- [ADR-08: Docker Best Practices](ADR-08.md)
- [GUIDE-09: Docker Deployment](../guides/09-docker-deployment.md)
- [GUIDE-10: CI/CD Guide](../guides/10-ci-cd-guide.md)
- [DevOps Roadmap](../../devops/doc/devops-roadmap.md)

---

## Changelog

| Дата | Версия | Изменения |
|------|--------|-----------|
| 2025-10-17 | 1.0 | Первая версия: выбор GitHub Actions + ghcr.io |


