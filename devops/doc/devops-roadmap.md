# DevOps Roadmap

## Overview

MVP-подход к внедрению DevOps процессов в проект. Фокус на простоте и скорости развертывания - от локального запуска через Docker до автоматического деплоя на удаленный сервер.

## Принципы

- **MVPFirst**: простота и скорость важнее преждевременной оптимизации
- **Iterative**: небольшие спринты с четкими целями
- **Plan Mode**: детальное планирование каждого спринта перед реализацией
- **Fast Path**: максимально быстрый путь от локальной разработки до production

## Sprint Overview

| Sprint | Description | Status | Plan |
|--------|-------------|--------|------|
| **D0** | Basic Docker Setup | 🟢 Completed | [sprint-d0-docker-setup.md](plans/sprint-d0-docker-setup.md) |
| **D1** | Build & Publish | 🟢 Completed | [sprint-d1-build-publish.md](plans/sprint-d1-build-publish.md) |
| **D2** | Развертывание на сервер | 🔵 Planned | - |
| **D3** | Auto Deploy | 🔵 Planned | - |

### Status Legend
- 🔵 Planned - запланирован
- 🟡 In Progress - в работе
- 🟢 Completed - выполнен
- 🔴 Blocked - заблокирован

---

## Sprint D0: Basic Docker Setup

### Цели
- Контейнеризировать все сервисы проекта
- Обеспечить запуск всего стека одной командой `docker-compose up`
- Создать воспроизводимое локальное окружение для разработки

### Состав работ
- Создать Dockerfile для Bot сервиса (Python + UV)
- Создать Dockerfile для API сервиса (FastAPI + UV)
- Создать Dockerfile для Frontend сервиса (Next.js + pnpm)
- Интегрировать существующий PostgreSQL контейнер в общий docker-compose.yml
- Создать .dockerignore файлы для оптимизации сборки
- Настроить сетевое взаимодействие между сервисами
- Обеспечить управление переменными окружения через .env
- Проверить полную работоспособность локального стека
- Обновить документацию с инструкциями по запуску

### Критерии готовности
- `docker-compose up` запускает все 4 сервиса
- Bot подключается к PostgreSQL и обрабатывает сообщения
- API отвечает на HTTP запросы
- Frontend доступен в браузере и взаимодействует с API
- Миграции БД выполняются автоматически

---

## Sprint D1: Build & Publish

**Статус:** ✅ **ЗАВЕРШЕН** (18.10.2025)  
**Отчет:** [d1-final-report.md](reports/d1-final-report.md)

### Цели
- Автоматизировать сборку Docker образов через GitHub Actions
- Публиковать образы в GitHub Container Registry (ghcr.io)
- Обеспечить версионирование образов через Git теги

### Состав работ
- Создать GitHub Actions workflow для сборки образов
- Настроить триггер на push в main ветку
- Реализовать сборку 3 образов (bot, api, frontend) параллельно
- Настроить авторизацию в ghcr.io через GitHub token
- Публиковать образы с тегами `latest` и Git SHA
- Создать инструкцию по настройке permissions для GitHub Container Registry
- Добавить badges статуса сборки в README
- Протестировать workflow на тестовом коммите

### Критерии готовности
- После push в main автоматически собираются 3 образа
- Образы успешно публикуются в ghcr.io
- Образы можно скачать командой `docker pull`
- В README отображаются актуальные badges

---

## Sprint D2: Развертывание на сервер

### Цели
- Развернуть приложение на удаленном сервере
- Создать пошаговую инструкцию для ручного деплоя
- Отработать все шаги развертывания и зафиксировать их

### Состав работ
- Создать детальную пошаговую инструкцию для ручного деплоя
- Описать процесс SSH подключения с использованием ключа
- Документировать копирование конфигурационных файлов
- Описать авторизацию в ghcr.io на удаленном сервере
- Создать инструкции по загрузке образов через `docker-compose pull`
- Описать запуск сервисов через `docker-compose up -d`
- Документировать процесс выполнения миграций БД
- Создать шаблон .env.production с описанием всех переменных
- Разработать скрипт проверки работоспособности сервисов
- Проверить полный цикл развертывания на реальном сервере

### Критерии готовности
- Существует детальная инструкция для деплоя
- Приложение успешно развернуто на сервере
- Все сервисы работают и доступны извне
- Документирован процесс отката (rollback)

---

## Sprint D3: Auto Deploy

### Цели
- Автоматизировать процесс развертывания через GitHub Actions
- Обеспечить безопасное подключение к серверу через SSH
- Создать удобный механизм деплоя "по кнопке"

### Состав работ
- Создать GitHub Actions workflow для автоматического деплоя
- Настроить триггер `workflow_dispatch` (ручной запуск)
- Реализовать SSH подключение через GitHub secrets
- Автоматизировать pull новых версий образов
- Автоматизировать перезапуск сервисов
- Добавить выполнение миграций в процесс деплоя
- Создать инструкцию по настройке GitHub secrets (SSH_KEY, HOST, USER)
- Реализовать уведомления о статусе деплоя (success/failure)
- Добавить в workflow health check после деплоя
- Обновить README с кнопкой "Deploy to Production"

### Критерии готовности
- Деплой запускается одной кнопкой в GitHub Actions
- Автоматически обновляются все сервисы на сервере
- В случае ошибки приходит уведомление
- Есть документация по настройке всех secrets

---

## Next Steps

После завершения базовых спринтов (D0-D3) возможны следующие улучшения:
- Мониторинг и логирование (Prometheus, Grafana, ELK)
- Автоматические тесты в CI/CD pipeline
- Blue-green или rolling deployments
- Автоматический rollback при ошибках
- Staging окружение
- Secrets management (Vault, SOPS)
- Resource limits и health checks
- Backup и disaster recovery

---

## Resources

### Documentation
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

### Project Files
- Docker configurations: `/` (root directory)
- GitHub workflows: `/.github/workflows/`
- Deployment guides: `/devops/doc/guides/`
- Sprint plans: `/devops/doc/plans/`

