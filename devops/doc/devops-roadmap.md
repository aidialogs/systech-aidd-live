# DevOps Roadmap

## Обзор

Данный roadmap описывает путь развития DevOps процессов для проекта systech-aidd-live. Фокус на MVP подходе: простота, скорость, без преждевременной оптимизации. Цель - пройти путь от локального запуска до автоматического развертывания на удаленном сервере максимально быстро.

## Спринты

| Код | Описание | Статус | План |
|-----|----------|--------|------|
| D0 | Basic Docker Setup | ✅ Completed | [Sprint D0 Plan](plans/sprint-d0-plan.md) |
| D1 | Build & Publish | ✅ Completed | [Sprint D1 Plan](plans/sprint-d1-plan.md) |
| D2 | Развертывание на сервер | 📝 Planned | - |
| D3 | Auto Deploy | 📝 Planned | - |

**Легенда статусов:**
- 📝 Planned - запланировано
- 🚧 In Progress - в работе
- ✅ Completed - завершено
- ⏸️ On Hold - приостановлено

---

## ✅ Спринт D0: Basic Docker Setup

**Статус:** ✅ Completed (18 октября 2025)

**Цель:** Запустить все сервисы локально через docker-compose одной командой.

**Выполненные работы:**
- ✅ Все Dockerfiles созданы в devops/Dockerfile.*
- ✅ Создан Dockerfile для каждого сервиса (bot, api, frontend)
- ✅ Создан docker-compose.yml с 4 сервисами (PostgreSQL, Bot, API, Frontend)
- ✅ docker-compose.yml размещен в devops/docker-compose.yml
- ✅ Созданы .dockerignore файлы для оптимизации сборки
- ✅ Настроено автоматическое применение миграций при запуске бота
- ✅ Создан шаблон .env файла (devops/env.example)
- ✅ Создана полная документация (DOCKER_QUICKSTART.md, TESTING.md)
- ✅ Обновлен README.md с инструкциями по запуску через Docker
- ✅ Создан Makefile для упрощения команд Docker

**Результат:** Все сервисы запускаются одной командой `docker compose up`

**Сервисы:**
1. **Bot** - Python + UV, Telegram бот, подключается к PostgreSQL
2. **API** - Python + UV, FastAPI сервис для статистики
3. **Frontend** - Next.js + pnpm, веб-интерфейс, подключается к API
4. **PostgreSQL** - база данных (уже существует в проекте)

**Документация:**
- [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md) - Полный гайд по запуску
- [TESTING.md](../TESTING.md) - Инструкция по тестированию
- [SPRINT_D0_COMPLETE.md](../SPRINT_D0_COMPLETE.md) - Отчет о завершении спринта

---

## ✅ Спринт D1: Build & Publish

**Статус:** ✅ Completed (18 октября 2025)

**Цель:** Автоматическая сборка и публикация Docker образов в GitHub Container Registry.

**Выполненные работы:**
- ✅ Создано введение в GitHub Actions (GITHUB_ACTIONS_INTRO.md)
- ✅ Создан GitHub Actions workflow (.github/workflows/build.yml)
- ✅ Настроены триггеры: PR (только build) и push в day6-ci-draft (build + publish)
- ✅ Реализована matrix strategy для параллельной сборки 3 образов
- ✅ Настроено кэширование Docker layers для ускорения сборки
- ✅ Образы публикуются с тегами: latest и sha-abc1234
- ✅ Создан docker-compose.registry.yml для использования образов из ghcr.io
- ✅ Создан docker-compose.override.example.yml для гибкого переключения
- ✅ Обновлен Makefile с командами для работы с registry
- ✅ Создана инструкция по настройке публичного доступа (REGISTRY_SETUP.md)
- ✅ Создана полная инструкция по CI/CD (CI_CD_USAGE.md)
- ✅ Обновлен README.md с badge и инструкциями по использованию образов
- ✅ Образы готовы к использованию в спринтах D2 и D3

**Результат:** Автоматическая сборка и публикация образов в ghcr.io через GitHub Actions.

**Образы:**
- `ghcr.io/<owner>/<repo>/bot:latest`
- `ghcr.io/<owner>/<repo>/api:latest`
- `ghcr.io/<owner>/<repo>/frontend:latest`

**Документация:**
- [GitHub Actions Intro](GITHUB_ACTIONS_INTRO.md) - Введение в GitHub Actions
- [Registry Setup](REGISTRY_SETUP.md) - Настройка публичного доступа
- [CI/CD Usage](CI_CD_USAGE.md) - Полное руководство по работе с CI/CD
- [Sprint D1 Complete](../SPRINT_D1_COMPLETE.md) - Отчет о завершении спринта

---

## D2: Развертывание на сервер

### Цели

Развернуть приложение на удаленном сервере вручную по пошаговой инструкции.

### Состав работ

- Создать детальную инструкцию для ручного деплоя (`doc/guides/manual-deploy.md`)
- Описать процесс SSH подключения к серверу с использованием SSH ключа
- Описать копирование docker-compose.yml и .env на сервер
- Описать аутентификацию в ghcr.io через docker login
- Описать загрузку образов через docker-compose pull
- Описать запуск сервисов через docker-compose up -d
- Описать запуск миграций базы данных
- Создать шаблон `.env.production` с описанием всех переменных
- Создать скрипт проверки работоспособности `scripts/deploy-check.sh`

---

## D3: Auto Deploy

### Цели

Автоматическое развертывание на сервер через GitHub Actions по нажатию кнопки.

### Состав работ

- Создать GitHub Actions workflow `.github/workflows/deploy.yml`
- Настроить trigger на ручной запуск (workflow_dispatch)
- Реализовать SSH подключение к серверу с использованием SSH ключа
- Реализовать pull новых версий образов
- Реализовать restart сервисов через docker-compose
- Создать инструкцию по настройке GitHub secrets (SSH_KEY, HOST, USER)
- Добавить уведомления о статусе деплоя
- Добавить кнопку "Deploy" в README.md

---

## Архитектура сервисов

Проект состоит из 4 сервисов:

1. **Bot** (Python + UV) - Telegram бот, подключается к PostgreSQL
2. **API** (Python + UV) - FastAPI сервис для статистики
3. **Frontend** (Next.js + pnpm) - веб-интерфейс, подключается к API
4. **PostgreSQL** - база данных (уже существует в проекте)

---

## Примечания

- План реализации каждого спринта создается в режиме Plan Mode
- После выполнения спринта ссылка на план добавляется в таблицу спринтов
- Планы хранятся в директории `devops/doc/plans/`
- Формат файла плана: `sprint-{код_спринта}-plan.md` (например, `sprint-d0-plan.md`)
