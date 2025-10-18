# DevOps Guides

Пошаговые руководства по DevOps процессам проекта systech-aidd-live.

## Доступные гайды

### ✅ Sprint D0: Basic Docker Setup

**Статус:** Выполнен

**Быстрый старт:**
1. [Docker Setup Summary](../../../DOCKER-SETUP-SUMMARY.md) - краткое руководство (5 минут)
2. [Sprint D0 Plan](../plans/sprint-d0-docker-setup.md) - детальный план реализации
3. [Main README - Docker Section](../../../README.md#-запуск-через-docker) - полная документация

**Что реализовано:**
- Контейнеризация всех сервисов (bot, api, frontend, postgres)
- Docker Compose конфигурация
- Makefile команды для управления
- Полная документация

**Быстрый запуск:**
```bash
cp env.docker.example .env
# (заполнить переменные)
make docker-up
docker compose exec api uv run alembic upgrade head
```

### 🔵 Sprint D1: Build & Publish (Запланирован)

**Цель:** Автоматическая сборка и публикация Docker образов через GitHub Actions

**Что будет:**
- Multi-stage builds
- GitHub Actions workflows
- GitHub Container Registry
- Автоматическое версионирование

**Когда:** После завершения D0

### 🔵 Sprint D2: Развертывание (Запланирован)

**Цель:** Развертывание на production сервере

**Что будет:**
- Инструкция по ручному деплою
- SSH настройка
- Production конфигурация
- Проверка работоспособности

**Когда:** После завершения D1

### 🔵 Sprint D3: Auto Deploy (Запланирован)

**Цель:** Автоматический деплой по кнопке

**Что будет:**
- GitHub Actions для деплоя
- Workflow dispatch
- Health checks
- Уведомления

**Когда:** После завершения D2

## Структура документации

```
devops/
├── README.md                           # Главная страница DevOps
├── doc/
│   ├── devops-roadmap.md              # Roadmap всех спринтов
│   ├── plans/                         # Детальные планы
│   │   └── sprint-d0-docker-setup.md
│   └── guides/                        # Пошаговые инструкции
│       └── README.md                  # Этот файл
└── scripts/                           # Скрипты автоматизации
```

## Быстрая навигация

| Документ | Описание | Уровень |
|----------|----------|---------|
| [DOCKER-SETUP-SUMMARY.md](../../../DOCKER-SETUP-SUMMARY.md) | Краткое руководство Docker | ⭐ Начинающий |
| [README.md - Docker](../../../README.md#-запуск-через-docker) | Полная документация Docker | Средний |
| [DevOps Roadmap](../devops-roadmap.md) | План всех спринтов | Обзор |
| [Sprint D0 Plan](../plans/sprint-d0-docker-setup.md) | Детальный план D0 | Продвинутый |
| [DevOps README](../../README.md) | Обзор инфраструктуры | Средний |

## Как использовать гайды

### Для новых разработчиков

1. Начните с [DOCKER-SETUP-SUMMARY.md](../../../DOCKER-SETUP-SUMMARY.md)
2. Следуйте инструкциям по быстрому старту
3. Изучите доступные команды в [Makefile](../../../Makefile)

### Для опытных разработчиков

1. Прочитайте [DevOps Roadmap](../devops-roadmap.md) для понимания общей картины
2. Изучите детальные планы в директории `plans/`
3. Следите за обновлениями в roadmap

### Для DevOps инженеров

1. Изучите [Sprint D0 Plan](../plans/sprint-d0-docker-setup.md) для понимания архитектурных решений
2. Ознакомьтесь с [DevOps README](../../README.md) для полного обзора
3. Планируйте следующие спринты на основе roadmap

## Полезные команды

### Docker

```bash
make docker-up              # Запуск всех сервисов
make docker-down            # Остановка
make docker-logs            # Просмотр логов
make docker-ps              # Статус сервисов
make docker-restart         # Перезапуск
```

### База данных

```bash
docker compose exec api uv run alembic upgrade head    # Миграции
docker compose exec postgres psql -U systech_user -d systech_aidd  # SQL консоль
```

### Отладка

```bash
docker compose logs -f api bot          # Логи backend
docker compose exec api /bin/bash       # Shell в контейнере
docker compose ps                       # Статус всех контейнеров
```

## FAQ

### Как запустить проект впервые?

См. [DOCKER-SETUP-SUMMARY.md](../../../DOCKER-SETUP-SUMMARY.md) - раздел "Быстрый старт"

### Что делать если порт занят?

Проверьте какой процесс использует порт:
```bash
lsof -i :8000  # для API
lsof -i :3000  # для Frontend
```

Остановите другой проект или измените порты в docker-compose.yml

### Как пересобрать образы после изменений?

```bash
make docker-build
make docker-restart
```

### Как очистить все Docker данные?

⚠️ **Внимание:** Это удалит все volumes (включая БД)!

```bash
make docker-clean
```

## Troubleshooting

### Проблемы с PostgreSQL

1. Проверьте healthcheck: `docker compose ps`
2. Проверьте логи: `make docker-logs-db`
3. Подключитесь к БД: `docker compose exec postgres psql -U systech_user -d systech_aidd`

### Frontend не подключается к API

Проверьте переменную `NEXT_PUBLIC_API_URL` в docker-compose.yml:
```yaml
environment:
  - NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Bot не запускается

1. Проверьте логи: `make docker-logs-bot`
2. Убедитесь что заполнены все переменные в .env
3. Проверьте что PostgreSQL запущен: `docker compose ps postgres`

## Вклад в документацию

При создании новых гайдов:
1. Следуйте структуре существующих документов
2. Используйте русский язык
3. Добавляйте примеры кода
4. Обновляйте этот README с ссылкой на новый гайд

## Контакты

Проект: **systech-aidd-2025**

---

**Начните с Docker:**
```bash
make docker-up
```
