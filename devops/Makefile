# Makefile для управления Docker окружением
# Все команды запускаются из директории devops/

.PHONY: help build up down restart logs clean test status pull up-registry down-registry

# По умолчанию показать справку
help:
	@echo "Доступные команды для Docker окружения:"
	@echo ""
	@echo "📦 Локальная сборка:"
	@echo "  make build        - Собрать все Docker образы"
	@echo "  make up           - Запустить все сервисы"
	@echo "  make down         - Остановить все сервисы"
	@echo "  make restart      - Перезапустить все сервисы"
	@echo ""
	@echo "🚀 Работа с Registry (ghcr.io):"
	@echo "  make pull         - Загрузить образы из GitHub Container Registry"
	@echo "  make up-registry  - Запустить сервисы из образов registry"
	@echo "  make down-registry - Остановить сервисы registry"
	@echo ""
	@echo "📝 Логи и отладка:"
	@echo "  make logs         - Показать логи всех сервисов"
	@echo "  make logs-bot     - Логи бота"
	@echo "  make logs-api     - Логи API"
	@echo "  make logs-frontend - Логи фронтенда"
	@echo "  make logs-db      - Логи базы данных"
	@echo ""
	@echo "🔧 Управление:"
	@echo "  make shell-bot    - Подключиться к контейнеру бота"
	@echo "  make shell-api    - Подключиться к контейнеру API"
	@echo "  make shell-db     - Подключиться к PostgreSQL"
	@echo "  make test         - Запустить тесты в контейнере bot"
	@echo ""
	@echo "🧹 Очистка:"
	@echo "  make clean        - Остановить и удалить все (включая volumes)"
	@echo "  make rebuild      - Пересобрать образы без кэша"
	@echo ""
	@echo "📊 Информация:"
	@echo "  make ps           - Показать статус контейнеров"
	@echo "  make status       - Красивый статус всех сервисов"
	@echo "  make stats        - Показать использование ресурсов"

# Сборка всех образов
build:
	docker compose build

# Запуск всех сервисов
up:
	docker compose up

# Запуск в фоновом режиме
up-daemon:
	docker compose up -d

# Остановка всех сервисов
down:
	docker compose down

# Перезапуск всех сервисов
restart:
	docker compose restart

# Логи всех сервисов
logs:
	docker compose logs -f

# Логи отдельных сервисов
logs-bot:
	docker compose logs -f bot

logs-api:
	docker compose logs -f api

logs-frontend:
	docker compose logs -f frontend

logs-db:
	docker compose logs -f postgres

# Shell в контейнерах
shell-bot:
	docker compose exec bot sh

shell-api:
	docker compose exec api sh

shell-db:
	docker compose exec postgres psql -U systech_user -d systech_aidd

# Запуск тестов в контейнере
test:
	docker compose exec bot uv run pytest tests/

# Полная очистка (включая volumes)
clean:
	docker compose down -v
	docker image prune -f

# Пересборка без кэша
rebuild:
	docker compose build --no-cache

# Статус контейнеров
ps:
	docker compose ps

# Использование ресурсов
stats:
	docker stats --no-stream

# Красивый статус всех сервисов
status:
	@echo ""
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║          🐳 Статус Docker сервисов - Systech AIDD           ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📊 Статус контейнеров:"
	@echo "────────────────────────────────────────────────────────────────"
	@docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "⚠️  Контейнеры не запущены"
	@echo ""
	@echo "🏥 Health Checks:"
	@echo "────────────────────────────────────────────────────────────────"
	@if docker compose ps | grep -q "systech-aidd-postgres.*healthy"; then \
		echo "  ✅ PostgreSQL     : healthy"; \
	elif docker compose ps | grep -q "systech-aidd-postgres.*Up"; then \
		echo "  ⏳ PostgreSQL     : starting..."; \
	else \
		echo "  ❌ PostgreSQL     : stopped"; \
	fi
	@if docker compose ps | grep -q "systech-aidd-bot.*Up"; then \
		echo "  ✅ Bot            : running"; \
	else \
		echo "  ❌ Bot            : stopped"; \
	fi
	@if docker compose ps | grep -q "systech-aidd-api.*Up"; then \
		echo "  ✅ API            : running"; \
	else \
		echo "  ❌ API            : stopped"; \
	fi
	@if docker compose ps | grep -q "systech-aidd-frontend.*Up"; then \
		echo "  ✅ Frontend       : running"; \
	else \
		echo "  ❌ Frontend       : stopped"; \
	fi
	@echo ""
	@echo "🌐 Доступность сервисов:"
	@echo "────────────────────────────────────────────────────────────────"
	@if curl -sf http://localhost:8000/health > /dev/null 2>&1; then \
		echo "  ✅ API Health     : http://localhost:8000/health"; \
	else \
		echo "  ❌ API Health     : недоступен"; \
	fi
	@if curl -sf http://localhost:8000/docs > /dev/null 2>&1; then \
		echo "  ✅ API Docs       : http://localhost:8000/docs"; \
	else \
		echo "  ❌ API Docs       : недоступен"; \
	fi
	@if curl -sf http://localhost:3000 > /dev/null 2>&1; then \
		echo "  ✅ Frontend       : http://localhost:3000"; \
	else \
		echo "  ❌ Frontend       : недоступен"; \
	fi
	@if docker compose exec -T postgres pg_isready -U systech_user -d systech_aidd > /dev/null 2>&1; then \
		echo "  ✅ Database       : localhost:5432"; \
	else \
		echo "  ❌ Database       : недоступна"; \
	fi
	@echo ""
	@echo "💾 База данных:"
	@echo "────────────────────────────────────────────────────────────────"
	@if docker compose exec -T postgres psql -U systech_user -d systech_aidd -c "SELECT COUNT(*) as users FROM users; SELECT COUNT(*) as messages FROM messages;" 2>/dev/null | grep -E "^\s+[0-9]+" | head -2 | awk 'NR==1{print "  👤 Пользователей  : " $$1} NR==2{print "  💬 Сообщений      : " $$1}'; then \
		:; \
	else \
		echo "  ⚠️  Нет доступа к БД или таблицы не созданы"; \
	fi
	@echo ""
	@echo "💻 Использование ресурсов:"
	@echo "────────────────────────────────────────────────────────────────"
	@docker stats --no-stream --format "  {{.Name}}: CPU {{.CPUPerc}} | RAM {{.MemUsage}}" 2>/dev/null | grep systech || echo "  ⚠️  Контейнеры не запущены"
	@echo ""
	@echo "📝 Полезные команды:"
	@echo "────────────────────────────────────────────────────────────────"
	@echo "  make logs         - Показать логи всех сервисов"
	@echo "  make logs-api     - Логи API"
	@echo "  make logs-bot     - Логи бота"
	@echo "  make restart      - Перезапустить сервисы"
	@echo "  make down         - Остановить сервисы"
	@echo ""

# ═══════════════════════════════════════════════════════════════
# Команды для работы с GitHub Container Registry
# ═══════════════════════════════════════════════════════════════

# Загрузить образы из ghcr.io
pull:
	@echo "📥 Загрузка образов из GitHub Container Registry..."
	docker compose -f docker-compose.registry.yml pull

# Запустить сервисы из образов registry
up-registry:
	@echo "🚀 Запуск сервисов из образов registry..."
	docker compose -f docker-compose.registry.yml up

# Запустить в фоновом режиме
up-registry-daemon:
	@echo "🚀 Запуск сервисов из образов registry (в фоне)..."
	docker compose -f docker-compose.registry.yml up -d

# Остановить сервисы registry
down-registry:
	docker compose -f docker-compose.registry.yml down

# Перезапустить сервисы registry
restart-registry:
	docker compose -f docker-compose.registry.yml restart

# Логи сервисов registry
logs-registry:
	docker compose -f docker-compose.registry.yml logs -f

