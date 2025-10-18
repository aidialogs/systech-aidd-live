#!/bin/bash
# ============================================
# Deploy Check Script
# systech-aidd-live
# ============================================
#
# Скрипт для проверки работоспособности развернутого приложения
# Проверяет все сервисы, health checks, доступность API и Frontend
#
# Использование:
#   chmod +x deploy-check.sh
#   ./deploy-check.sh
#

set -e  # Выход при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Конфигурация
COMPOSE_FILE="docker-compose.prod.yml"
SERVICES=("postgres" "bot" "api" "frontend")
API_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:3000"
HEALTH_ENDPOINT="/health"
DOCS_ENDPOINT="/docs"

# Функции для вывода
print_header() {
    echo -e "\n${BLUE}============================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Проверка что Docker работает
check_docker() {
    print_header "Проверка Docker"
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker не установлен"
        exit 1
    fi
    print_success "Docker установлен: $(docker --version)"
    
    if ! docker info &> /dev/null; then
        print_error "Docker daemon не запущен"
        exit 1
    fi
    print_success "Docker daemon запущен"
    
    if ! command -v docker compose &> /dev/null; then
        print_error "Docker Compose не установлен"
        exit 1
    fi
    print_success "Docker Compose установлен: $(docker compose version)"
}

# Проверка что compose файл существует
check_compose_file() {
    print_header "Проверка файлов конфигурации"
    
    if [ ! -f "$COMPOSE_FILE" ]; then
        print_error "Файл $COMPOSE_FILE не найден"
        exit 1
    fi
    print_success "Найден $COMPOSE_FILE"
    
    if [ ! -f ".env" ]; then
        print_warning ".env файл не найден (может быть необходим для некоторых переменных)"
    else
        print_success "Найден .env файл"
    fi
}

# Проверка запущенных контейнеров
check_containers() {
    print_header "Проверка контейнеров"
    
    echo -e "${BLUE}Список контейнеров:${NC}"
    docker compose -f "$COMPOSE_FILE" ps
    echo ""
    
    local all_running=true
    
    for service in "${SERVICES[@]}"; do
        local container_name="systech-aidd-$service"
        local status=$(docker inspect -f '{{.State.Status}}' "$container_name" 2>/dev/null || echo "not_found")
        
        if [ "$status" = "running" ]; then
            print_success "Контейнер $container_name запущен"
        elif [ "$status" = "not_found" ]; then
            print_error "Контейнер $container_name не найден"
            all_running=false
        else
            print_error "Контейнер $container_name в статусе: $status"
            all_running=false
        fi
    done
    
    if [ "$all_running" = false ]; then
        print_error "Не все контейнеры запущены"
        return 1
    fi
}

# Проверка health checks
check_health() {
    print_header "Проверка Health Checks"
    
    local all_healthy=true
    
    # PostgreSQL
    if docker compose -f "$COMPOSE_FILE" exec -T postgres pg_isready -U systech_user -d systech_aidd &> /dev/null; then
        print_success "PostgreSQL: healthy"
    else
        print_error "PostgreSQL: unhealthy"
        all_healthy=false
    fi
    
    # API health endpoint
    sleep 2  # Даем время на запуск
    if curl -f -s "${API_URL}${HEALTH_ENDPOINT}" > /dev/null 2>&1; then
        print_success "API health check: OK"
        local health_response=$(curl -s "${API_URL}${HEALTH_ENDPOINT}")
        print_info "Response: $health_response"
    else
        print_error "API health check: FAILED"
        all_healthy=false
    fi
    
    # Frontend
    if curl -f -s "$FRONTEND_URL" > /dev/null 2>&1; then
        print_success "Frontend: доступен"
    else
        print_error "Frontend: недоступен"
        all_healthy=false
    fi
    
    if [ "$all_healthy" = false ]; then
        print_error "Не все сервисы прошли health check"
        return 1
    fi
}

# Проверка логов на ошибки
check_logs() {
    print_header "Проверка логов (последние 20 строк)"
    
    local has_errors=false
    
    for service in "${SERVICES[@]}"; do
        echo -e "\n${BLUE}--- Логи $service ---${NC}"
        local logs=$(docker compose -f "$COMPOSE_FILE" logs --tail=20 "$service" 2>&1)
        
        # Проверка на критичные ошибки
        if echo "$logs" | grep -iE "error|critical|fatal|exception" | grep -v "ERROR: for" > /dev/null; then
            print_warning "Найдены ошибки в логах $service:"
            echo "$logs" | grep -iE "error|critical|fatal|exception" | tail -5
            has_errors=true
        else
            print_success "Критичных ошибок не найдено в логах $service"
        fi
    done
    
    if [ "$has_errors" = true ]; then
        print_warning "Обнаружены ошибки в логах (это может быть нормально для некоторых случаев)"
    fi
}

# Проверка доступности API endpoints
check_api_endpoints() {
    print_header "Проверка API Endpoints"
    
    # Health
    if curl -f -s "${API_URL}${HEALTH_ENDPOINT}" > /dev/null; then
        print_success "GET ${API_URL}${HEALTH_ENDPOINT} - OK"
    else
        print_error "GET ${API_URL}${HEALTH_ENDPOINT} - FAILED"
    fi
    
    # Docs
    if curl -f -s "${API_URL}${DOCS_ENDPOINT}" > /dev/null; then
        print_success "GET ${API_URL}${DOCS_ENDPOINT} - OK"
    else
        print_warning "GET ${API_URL}${DOCS_ENDPOINT} - FAILED (может быть отключено в production)"
    fi
    
    # Root
    if curl -f -s "${API_URL}/" > /dev/null; then
        print_success "GET ${API_URL}/ - OK"
    else
        print_warning "GET ${API_URL}/ - FAILED"
    fi
}

# Проверка использования ресурсов
check_resources() {
    print_header "Использование ресурсов"
    
    echo -e "${BLUE}Docker stats (текущий момент):${NC}"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" $(docker compose -f "$COMPOSE_FILE" ps -q)
}

# Проверка volumes
check_volumes() {
    print_header "Проверка Volumes"
    
    local volumes=("devops_postgres_data" "devops_bot_logs" "devops_api_logs")
    
    for volume in "${volumes[@]}"; do
        if docker volume inspect "$volume" &> /dev/null; then
            local size=$(docker volume inspect "$volume" --format '{{ .Mountpoint }}' | xargs du -sh 2>/dev/null | awk '{print $1}' || echo "N/A")
            print_success "Volume $volume существует (размер: $size)"
        else
            print_warning "Volume $volume не найден"
        fi
    done
}

# Проверка сети
check_network() {
    print_header "Проверка Docker Network"
    
    local network="devops_systech-network"
    
    if docker network inspect "$network" &> /dev/null; then
        print_success "Network $network существует"
        local containers=$(docker network inspect "$network" --format '{{range .Containers}}{{.Name}} {{end}}')
        print_info "Подключенные контейнеры: $containers"
    else
        print_error "Network $network не найден"
    fi
}

# Итоговый отчет
print_summary() {
    print_header "Итоговый отчет"
    
    echo -e "${GREEN}Все основные проверки пройдены!${NC}\n"
    
    print_info "API доступен по адресу: ${API_URL}"
    print_info "API Docs: ${API_URL}/docs"
    print_info "Frontend: ${FRONTEND_URL}"
    
    echo ""
    print_info "Полезные команды:"
    echo "  Логи всех сервисов: docker compose -f $COMPOSE_FILE logs -f"
    echo "  Логи API: docker compose -f $COMPOSE_FILE logs -f api"
    echo "  Статус: docker compose -f $COMPOSE_FILE ps"
    echo "  Перезапуск: docker compose -f $COMPOSE_FILE restart"
    echo "  Остановка: docker compose -f $COMPOSE_FILE down"
}

# Основная функция
main() {
    print_header "🚀 Проверка развертывания systech-aidd-live"
    
    # Выполняем все проверки
    check_docker || exit 1
    check_compose_file || exit 1
    check_containers || exit 1
    check_health || exit 1
    check_api_endpoints || exit 1
    check_logs
    check_resources
    check_volumes
    check_network
    
    # Итог
    print_summary
    
    echo ""
    print_success "✓ Развертывание успешно! Все сервисы работают."
}

# Запуск
main "$@"

