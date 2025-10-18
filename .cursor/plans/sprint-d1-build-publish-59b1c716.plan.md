<!-- 59b1c716-ecc4-4136-8d69-106eaf466405 88b53a0b-6c20-4072-a345-86435dcb22b9 -->
# Спринт D1: Build & Publish

## Обзор

Автоматизация сборки и публикации Docker образов в GitHub Container Registry (ghcr.io). Образы будут собираться при каждом PR (проверка), а публиковаться при push в тестовую ветку для последующего использования в спринтах D2 (ручной deploy) и D3 (авто deploy).

## Основные файлы для создания/изменения

### 1. Введение в GitHub Actions

**Файл:** `devops/doc/GITHUB_ACTIONS_INTRO.md` (новый)

Краткая справка на русском языке:

- Что такое GitHub Actions и workflow
- Основные концепции: events, jobs, steps, runners
- Триггеры (push, pull_request, workflow_dispatch)
- Matrix strategy для параллельной сборки
- Работа с Docker и GitHub Container Registry
- Публичные vs приватные образы в ghcr.io
- Как работать с Pull Request (создание, проверка, merge)

### 2. GitHub Actions Workflow

**Файл:** `.github/workflows/build.yml` (новый)

Workflow с двумя режимами работы:

**Триггеры:**

- `pull_request` - только сборка образов (без публикации) для проверки
- `push` на ветку `day6-ci-draft` - сборка и публикация образов

**Jobs:**

**Job 1: build-and-push**

- Runs-on: ubuntu-latest
- Matrix strategy для 3 сервисов:
  ```yaml
  matrix:
    service: [bot, api, frontend]
  ```


**Steps:**

1. Checkout кода
2. Setup Docker Buildx
3. Кэширование Docker layers (для bot и api)
4. Login в GitHub Container Registry (ghcr.io) - только для push, не для PR
5. Извлечение metadata (теги, labels)
6. Build и Push образа:

   - Для PR: только build
   - Для push: build + push с тегами:
     - `latest`
     - Commit SHA (короткий): `sha-abc1234`

**Контекст для каждого сервиса:**

- bot: context `.`, dockerfile `devops/Dockerfile.bot`
- api: context `.`, dockerfile `devops/Dockerfile.api`  
- frontend: context `frontend`, dockerfile `devops/Dockerfile.frontend`

**Имя образа:** `ghcr.io/${{ github.repository }}/<service>:latest`

**Кэширование:**

- type=gha для GitHub Actions cache
- Кэшируются слои для ускорения повторных сборок

### 3. Настройка публичного доступа к образам

**Файл:** `devops/doc/REGISTRY_SETUP.md` (новый)

Инструкция по настройке публичного доступа:

1. После первой публикации образов перейти в Packages на GitHub
2. Для каждого пакета (bot, api, frontend):

   - Settings → Danger Zone → Change visibility
   - Выбрать "Public"

3. Это позволит скачивать образы без авторизации

**Примечание:** Публикация в ghcr.io происходит автоматически через GITHUB_TOKEN.

### 4. Интеграция с docker-compose

**Стратегия:** Создать отдельные docker-compose файлы для разных сценариев.

**Существующий файл:** `devops/docker-compose.yml`

- Остается для локальной разработки с build из исходников

**Новый файл:** `devops/docker-compose.registry.yml`

- Использует предсобранные образы из ghcr.io
- Вместо `build:` использует `image: ghcr.io/owner/repo/service:latest`
- Все остальные настройки (environment, volumes, networks) идентичны

**Новый файл:** `devops/docker-compose.override.example.yml`

- Пример для локального переопределения (не в git)
- Показывает как легко переключаться между local и registry

**Обновить:** `devops/Makefile`

- Добавить команды:
  - `make up-registry` - запуск с образами из registry
  - `make pull` - загрузка образов из registry
  - Обновить `make help` с новыми командами

### 5. Тестирование workflow

**Сценарии тестирования:**

1. **Проверка сборки на PR:**

   - Создать PR с небольшим изменением
   - Убедиться что workflow запускается
   - Проверить что образы собираются, но не публикуются
   - Проверить логи в GitHub Actions

2. **Публикация при push:**

   - Push в ветку `day6-ci-draft`
   - Убедиться что workflow собирает и публикует образы
   - Проверить что образы появились в GitHub Packages

3. **Локальная проверка pull из registry:**
   ```bash
   cd devops
   docker pull ghcr.io/owner/repo/bot:latest
   docker pull ghcr.io/owner/repo/api:latest
   docker pull ghcr.io/owner/repo/frontend:latest
   ```

4. **Запуск через docker-compose с registry:**
   ```bash
   cd devops
   docker compose -f docker-compose.registry.yml up
   ```


### 6. Документация

**Обновить:** `README.md`

Добавить в начало файла badge со статусом сборки:

```markdown
[![Build and Push Docker Images](https://github.com/owner/repo/actions/workflows/build.yml/badge.svg)](https://github.com/owner/repo/actions/workflows/build.yml)
```

Добавить секцию "🚀 Использование готовых образов из Registry":

- Как загрузить образы из ghcr.io
- Как запустить через `docker-compose.registry.yml`
- Ссылки на образы в GitHub Packages

**Создать:** `devops/doc/CI_CD_USAGE.md` (новый)

Полная инструкция по работе с CI/CD:

- Как работает workflow
- Как проверить сборку в PR
- Как опубликовать новые образы (push в ветку)
- Как использовать образы локально
- Troubleshooting

**Обновить:** `devops/doc/devops-roadmap.md`

- Изменить статус D1 на "✅ Completed"
- Добавить ссылку на план: `devops/doc/plans/sprint-d1-plan.md`

**Создать:** `devops/SPRINT_D1_COMPLETE.md` (после завершения)

- Отчет о выполнении спринта по аналогии с D0

### 7. Готовность к спринтам D2 и D3

**Для D2 (Ручной deploy):**

- Образы в ghcr.io готовы к использованию
- docker-compose.registry.yml можно скопировать на сервер
- Образы публичные, не требуют авторизации при pull

**Для D3 (Auto deploy):**

- Workflow уже настроен для сборки
- Можно расширить или создать отдельный workflow для deploy
- Образы тегируются SHA для версионирования

## Последовательность выполнения

1. Создать документацию по GitHub Actions (GITHUB_ACTIONS_INTRO.md)
2. Создать workflow файл (.github/workflows/build.yml)
3. Создать docker-compose.registry.yml для использования образов из registry
4. Обновить Makefile с командами для работы с registry
5. Создать инструкцию по настройке публичного доступа (REGISTRY_SETUP.md)
6. Протестировать workflow на PR (только build)
7. Протестировать публикацию при push в day6-ci-draft
8. Сделать образы публичными в GitHub Packages
9. Локально протестировать pull и запуск образов из registry
10. Обновить README.md с badge и инструкциями
11. Создать CI_CD_USAGE.md с полной документацией
12. Обновить devops-roadmap.md
13. Создать SPRINT_D1_COMPLETE.md

## Примечания

**MVP подход:**

- Простой workflow без излишних оптимизаций
- Базовое кэширование для ускорения
- Публичные образы для простоты доступа
- Минимум настроек и конфигурации

**НЕ включаем (для будущих спринтов):**

- Lint checks в workflow
- Tests в workflow
- Security scanning (Trivy, Snyk)
- Multi-platform builds (arm64, amd64)
- Автоматический deploy
- Notifications в Telegram/Slack
- Release management с semantic versioning

**Особенности реализации:**

- Matrix strategy минимизирует дублирование кода
- Кэширование layer-ов ускоряет повторные сборки
- Отдельные docker-compose файлы сохраняют гибкость
- Публичные образы упрощают использование

### To-dos

- [ ] Создать devops/doc/GITHUB_ACTIONS_INTRO.md с введением в GitHub Actions
- [ ] Создать .github/workflows/build.yml с matrix strategy для 3 сервисов
- [ ] Создать devops/docker-compose.registry.yml для использования образов из ghcr.io
- [ ] Обновить devops/Makefile с командами для работы с registry
- [ ] Создать devops/doc/REGISTRY_SETUP.md с инструкцией по настройке публичного доступа
- [ ] Протестировать workflow на PR (только build без публикации)
- [ ] Протестировать публикацию при push в day6-ci-draft
- [ ] Сделать образы публичными в GitHub Packages
- [ ] Локально протестировать pull и запуск образов из registry
- [ ] Обновить README.md с badge статуса сборки и инструкциями по использованию образов
- [ ] Создать devops/doc/CI_CD_USAGE.md с полной инструкцией по работе с CI/CD
- [ ] Обновить devops/doc/devops-roadmap.md со статусом D1
- [ ] Создать devops/SPRINT_D1_COMPLETE.md с отчетом о завершении спринта