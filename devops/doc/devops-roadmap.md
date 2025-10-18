# DevOps Roadmap

## Overview

Этот документ описывает план развития DevOps процессов для проекта AIDD Live. 

**Текущая версия проекта:** Telegram Bot MVP (минимальная версия)
- ✅ Telegram Bot с LLM интеграцией
- 📋 FastAPI Backend (запланирован)
- 📋 Next.js Frontend (запланирован)

## Sprints Overview

| Sprint | Description | Status | Date Completed |
|--------|-------------|--------|----------------|
| **D1** | Docker Image for Bot & Best Practices | 📋 Planned | - |
| **D2** | CI Pipeline Setup | 📋 Planned | - |
| **D3** | CD Pipeline & Deployment | 📋 Planned | - |

**Статусы:**
- 📋 Planned - Запланирован
- 🏗️ In Progress - В работе
- ✅ Done - Завершен

---

## Sprint D1: Docker Image for Bot & Best Practices

### Цели
- Создать production-ready Docker образ для Telegram бота
- Применить SOTA практики контейнеризации
- Оптимизировать образ для использования в CI/CD
- Обеспечить локальную проверку работоспособности
- Подготовить базу для будущего добавления API и Frontend сервисов

### Состав работ

**1. Dockerfile для Bot (Python + UV)**
- Multi-stage build для минимизации размера образа
- Использование UV для управления зависимостями (10-20x быстрее pip)
- Оптимизация слоев для кэширования
- Non-root пользователь для безопасности
- Health checks
- Базовый образ: python:3.11-slim

**2. Docker Compose для локальной разработки**
- Оркестрация бота
- Environment variables management
- Volume mounts для development режима
- Logs persistence
- Подготовка для будущих сервисов (API, Frontend, PostgreSQL)

**3. Best Practices & Documentation**
- ADR по лучшим практикам контейнеризации
- `.dockerignore` файл
- Hadolint проверки (Dockerfile linter)
- Security scanning (Trivy)
- Build time optimization
- Документация по локальному запуску и проверке работоспособности
- Интеграция Docker команд в Makefile

### 📋 Планируемые результаты Sprint D1

**Статус:** Запланировано
**Целевая дата:** TBD

**Что будет создано:**
- [ ] `.dockerignore` - исключение ненужных файлов из контекста сборки
- [ ] `devops/Dockerfile.bot` - Multi-stage build для Telegram бота (Python 3.11-slim + UV)
- [ ] `devops/docker-compose.yml` - Базовая оркестрация для бота
- [ ] `devops/docker-compose.dev.yml` - Development overrides с volume mounts
- [ ] `devops/.hadolint.yaml` - Конфигурация Hadolint для проверки Dockerfile
- [ ] `doc/adrs/ADR-06.md` - Документация архитектурных решений по Docker (для MVP бота)
- [ ] `Makefile` - Добавить Docker-команды (docker-build, docker-up, docker-down, docker-logs, docker-clean)
- [ ] `README.md` - Добавить секцию "🐳 Docker Deployment"

**Целевые характеристики:**
- Multi-stage build для минимизации размера образа
- Non-root пользователь (`appuser` UID 1001) для безопасности
- Health check для бота (проверка работоспособности)
- UV для ускорения установки Python-зависимостей (10-20x быстрее pip)
- Development режим с volume mounts для hot reload
- Централизация Docker-инфраструктуры в папке `devops/`
- Hadolint для проверки качества Dockerfile

**Планируемые Makefile команды:**
```bash
make docker-build       # Сборка образа бота
make docker-up          # Запуск в production режиме
make docker-dev         # Запуск в dev режиме (hot reload)
make docker-down        # Остановка сервиса
make docker-logs        # Просмотр логов
make docker-restart     # Перезапуск
make docker-clean       # Очистка (containers + volumes)
make docker-lint        # Hadolint проверка
```

**Планируемые архитектурные решения (ADR-06):**
1. Multi-stage builds для оптимизации размера и безопасности
2. UV вместо pip для ускорения установки зависимостей
3. Non-root пользователь и минимальный base image (python:3.11-slim)
4. Health check для мониторинга состояния бота
5. Docker Compose для локальной разработки и тестирования
6. Development vs Production конфигурации через compose overrides
7. Централизация в `devops/` для будущего расширения (API, Frontend)
8. Подготовка для публикации в container registry (ghcr.io, Docker Hub)

**Целевые метрики:**
- Размер образа: ~150-180MB (с UV и slim base)
- Build time: < 2 минуты (с кэшированием < 30 секунд)
- Security: 0 критичных уязвимостей (Hadolint проверка)
- Совместимость: amd64 и arm64 архитектуры

**Готовность к следующему спринту:**
- Образ готов для публикации в registry
- Dockerfile оптимизирован для CI/CD
- Документация создана
- Локальная разработка полностью функциональна

---

## Sprint D2: CI Pipeline Setup

### Цели
- Настроить автоматизированный CI pipeline
- Обеспечить качество кода на всех этапах
- Автоматизировать сборку и тестирование образов
- Интегрировать security scanning
- Настроить публикацию образов в registry

### Состав работ

**1. Выбор и настройка CI инструмента**
- Анализ вариантов: GitHub Actions vs GitLab CI vs другие облачные CI/CD сервисы
- Выбор оптимального решения для проекта
- Базовый гайл по GithubActions workflow для CI/CD
- Базовая настройка workflow/pipeline
- Настройка triggers и условий запуска

**2. Job: Lint & Type Check**
- **Bot Service**: 
  - Ruff для linting Python кода
  - mypy для type checking (strict mode)
  - pytest для unit тестов (без integration тестов в CI)
  - Coverage check (требование 90%+)

**3. Job: Integration Tests (optional)**
- Интеграционный тест бота (с реальным LLM API)
- Проверка работоспособности основных функций
- Health check проверки

**4. Job: Build Docker Image**
- Сборка образа для Telegram бота
- Использование Docker BuildKit
- Layer caching для ускорения
- Tagging стратегия (commit SHA, branch, latest)
- Multi-platform builds (amd64, arm64) - опционально

**5. Job: Security Scan**
- Сканирование Docker образа (Trivy)
- Проверка уязвимостей Python зависимостей
- Настройка порогов severity
- Fail pipeline при критических уязвимостях

**6. Job: Publish Image**
- Публикация в Container Registry (GitHub Container Registry рекомендуется)
- Только при push в main branch
- Версионирование образа (semver + commit SHA)
- Cleanup старых образов (keep last 10)
- Tag latest для последнего стабильного релиза

---

## Sprint D3: CD Pipeline & Deployment

### Цели
- Автоматизировать процесс развертывания
- Настроить безопасное подключение к production серверу
- Обеспечить zero-downtime deployments
- Настроить мониторинг и rollback механизмы
- Документировать процесс deployment

### Состав работ

**1. Подготовка Production сервера**
- Проверка готовности сервера (VPS/Cloud VM)
- Установка необходимого ПО (Docker, Docker Compose)
- Настройка firewall и security groups
- Создание deployment пользователя с ограниченными правами
- SSH key-based authentication

**2. Ручное развертывание (проверка)**
- SSH подключение к серверу
- Копирование docker-compose.yml
- Настройка .env файла с секретами (BOT_TOKEN, LLM_API_KEY)
- Ручной запуск бота
- Проверка работоспособности через Telegram
- Документирование процесса

**3. GitHub Actions Deploy Job**
- SSH подключение из GitHub Actions
- Secure secrets management (GitHub Secrets для BOT_TOKEN, LLM_API_KEY)
- Pull образа из Container Registry
- Автоматизация deployment команд
- Health checks после deployment
- Graceful shutdown старого контейнера

**4. Deployment стратегия**
- Rolling update (pull новый образ → stop старый → start новый)
- Graceful shutdown (бот корректно завершает обработку сообщений)
- Restart policy (always) для автоматического восстановления
- Логирование в файл (persistency через volumes)

**5. Мониторинг и Rollback**
- Post-deployment health checks (проверка логов)
- Manual smoke test через Telegram
- Rollback механизм: откат на предыдущий образ
- Logging setup (logs volume mount)
- Basic alerting (email/Telegram уведомления при падении)

**6. Secrets Management**
- GitHub Secrets для хранения:
  - BOT_TOKEN (Telegram)
  - LLM_API_KEY (OpenRouter/OpenAI)
  - SSH_PRIVATE_KEY (для deployment)
  - SERVER_HOST и SERVER_USER
- .env файл генерируется на сервере из secrets
- Secrets rotation: вручную через GitHub UI

**7. Documentation & Runbooks**
- Deployment инструкции (step-by-step)
- Troubleshooting guide (типичные проблемы и решения)
- Rollback процедуры (как откатить на предыдущую версию)
- Manual deployment fallback (если CI/CD не работает)
- Contact info для экстренных ситуаций

---

## Future Enhancements

После завершения основных спринтов, возможные улучшения:

- **Monitoring & Observability**: Prometheus, Grafana, Loki
- **Auto-scaling**: Kubernetes migration
- **Multi-environment**: Staging, Preview environments
- **Performance Testing**: Load testing в CI
- **Infrastructure as Code**: Terraform/Ansible
- **Cost Optimization**: Image size reduction, compute optimization
- **Compliance**: Security audits, compliance checks

---

## Notes

- Все спринты выполняются в режиме **Plan Mode**
- После завершения каждого спринта создается детальный план-отчет
- Ссылка на план добавляется в таблицу Overview
- Приоритет - безопасность и стабильность
- Следуем best practices и SOTA подходам

