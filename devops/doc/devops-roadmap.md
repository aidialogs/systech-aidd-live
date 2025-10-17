# DevOps Roadmap

## Overview

Этот документ описывает план развития DevOps процессов для проекта AIDD Live. Проект включает три основных сервиса: Telegram Bot, FastAPI Backend и Next.js Frontend.

## Sprints Overview

| Sprint | Description | Status | Plan |
|--------|-------------|--------|------|
| **D1** | Docker Images & Best Practices | 📋 Planned | - |
| **D2** | CI Pipeline Setup | 📋 Planned | - |
| **D3** | CD Pipeline & Deployment | 📋 Planned | - |

**Статусы:**
- 📋 Planned - Запланирован
- 🏗️ In Progress - В работе
- ✅ Done - Завершен

---

## Sprint D1: Docker Images & Best Practices

### Цели
- Создать production-ready Docker образы для всех сервисов
- Применить SOTA практики контейнеризации
- Оптимизировать образы для использования в CI/CD
- Обеспечить локальную проверку работоспособности
- Учесть плоскую структуру проекта (бот и API в одном проекте)
- Учесть наличие docker-compose.yml для БД PostgreSQL

### Состав работ

**1. Dockerfile для Bot (Python + UV)**
- Multi-stage build для минимизации размера образа
- Использование UV для управления зависимостями
- Оптимизация слоев для кэширования
- Non-root пользователь для безопасности
- Health checks

**2. Dockerfile для API (FastAPI + UV)**
- Multi-stage build с отдельными этапами для зависимостей и runtime
- Использование UV для быстрой установки зависимостей
- Оптимизация для быстрых пересборок
- Настройка Uvicorn для production
- Health endpoints и проверки
- Security hardening (non-root, минимальные права)

**3. Dockerfile для Frontend (Next.js + pnpm)**
- Multi-stage build с node_modules кэшированием
- Standalone output для минимального runtime образа
- Использование pnpm для эффективного управления зависимостями
- Оптимизация статических ресурсов
- Security headers и настройки

**4. Docker Compose для локальной разработки**
- Orchestration всех сервисов
- Настройка сети и volumes
- Environment variables management
- PostgreSQL service
- Hot reload для разработки

**5. Best Practices & Documentation**
- ADR по лучшим практикам контейнеризации
- .dockerignore файлы
- Hadolint проверки (Dockerfile linter)
- Security scanning (Trivy)
- Build time optimization
- Документация по локальному запуску

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

**2. Jobs: Lint & Type Check (параллельно)**
- **Bot Service**: 
  - Ruff для linting Python кода
  - mypy для type checking
  - pytest для unit тестов
- **API Service**: 
  - Ruff для linting
  - mypy для type checking  
  - pytest для API тестов
- **Frontend Service**:
  - ESLint для JavaScript/TypeScript
  - TypeScript compiler проверки
  - Prettier для форматирования

**3. Job: Smoke Tests**
- Базовые интеграционные тесты
- Проверка взаимодействия сервисов
- Database migrations testing
- API endpoints health checks

**4. Job: Build Docker Images**
- Параллельная сборка образов для всех сервисов
- Использование Docker BuildKit
- Layer caching для ускорения
- Tagging стратегия (commit SHA, branch, latest)
- Multi-platform builds (amd64, arm64)

**5. Job: Security Scan**
- Сканирование Docker образов (Trivy, Snyk)
- Проверка уязвимостей зависимостей
- SBOM (Software Bill of Materials) генерация
- Настройка порогов severity
- Fail pipeline при критических уязвимостях

**6. Job: Publish Images**
- Публикация в Container Registry (GitHub Container Registry / Docker Hub)
- Только при push в main/production branches
- Версионирование образов
- Cleanup старых образов
- Генерация release notes

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
- Проверка готовности сервера
- Установка необходимого ПО (Docker, Docker Compose)
- Настройка firewall и security groups
- Создание deployment пользователя с ограниченными правами
- SSH key-based authentication

**2. Ручное развертывание (проверка)**
- SSH подключение к серверу
- Копирование docker-compose.yml
- Настройка .env файлов и secrets
- Ручной запуск сервисов
- Проверка работоспособности
- Документирование процесса

**3. GitHub Actions Deploy Job**
- SSH подключение из GitHub Actions
- Secure secrets management (GitHub Secrets)
- Копирование необходимых файлов
- Автоматизация deployment команд
- Health checks после deployment

**4. Deployment стратегии**
- Blue-Green deployment strategy
- Rolling updates
- Graceful shutdown существующих контейнеров
- Database migrations автоматизация
- Backup перед deployment

**5. Мониторинг и Rollback**
- Post-deployment health checks
- Automated smoke tests на production
- Rollback механизм при failures
- Logging и alerting setup
- Metrics collection (опционально: Prometheus)

**6. Secrets и Configuration Management**
- Environment-specific configurations
- Secure secrets storage (GitHub Secrets, Vault)
- .env files генерация
- Database credentials rotation
- API keys management

**7. Documentation & Runbooks**
- Deployment инструкции
- Troubleshooting guide
- Rollback процедуры
- Emergency contacts
- Incident response plan

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

