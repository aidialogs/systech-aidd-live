# Спринт D2: Развертывание на сервер - Статус

**Дата начала:** 18 октября 2025  
**Статус:** 🔄 В процессе (70% выполнено)

---

## Прогресс

### ✅ Завершенные задачи

#### 1. Проверка сервера

**Выполнено:**
- ✅ Проверен SSH доступ к серверу 90.156.229.75
- ✅ Подтверждена установка Docker 28.5.1
- ✅ Подтверждена установка Docker Compose v2.40.1
- ✅ Проверен порт 22 (SSH) - открыт

**Требуется:**
- ⚠️ Открыть порт 3000 (Frontend)
- ⚠️ Открыть порт 8000 (API)
- ℹ️ Порт 5432 (PostgreSQL) должен остаться закрытым (только внутри Docker)

#### 2. Создание файлов конфигурации

**✅ devops/.env.production.example**
- Все переменные окружения описаны
- Добавлены комментарии на русском
- Описана безопасность и best practices
- Checklist перед деплоем
- Рекомендации по генерации паролей

**✅ devops/docker-compose.prod.yml**
- Использует образы из `ghcr.io/aidialogs/systech-aidd-live`
- PostgreSQL: порты НЕ открыты наружу (безопасность)
- Frontend: `NEXT_PUBLIC_API_URL=http://90.156.229.75:8000`
- Все сервисы: `restart: always`
- Health checks для api и frontend
- Ограничения ресурсов (memory limits)
- Подробные комментарии

**✅ devops/deploy-check.sh**
- Автоматическая проверка всех сервисов
- Проверка Docker и Docker Compose
- Проверка контейнеров и health checks
- Проверка API endpoints
- Проверка логов на ошибки
- Проверка ресурсов (CPU, Memory)
- Цветной вывод для удобства
- Сделан исполняемым (chmod +x)

#### 3. Документация

**✅ doc/guides/manual-deploy.md (800+ строк)**

Создана подробная пошаговая инструкция:
- Введение и архитектура
- Предварительные требования
- Подготовка локально (создание .env)
- Подключение к серверу (SSH с ключом)
- Подготовка сервера (директории, порты, firewall)
- Копирование файлов (scp команды ready-to-copy)
- Загрузка Docker образов (docker compose pull)
- Запуск сервисов (docker compose up -d)
- Запуск миграций (alembic upgrade head)
- Проверка работоспособности (автоматическая и ручная)
- Управление сервисами (restart, logs, etc.)
- **Troubleshooting (10+ типовых проблем с решениями)**
- Безопасность (firewall, права, бэкапы)
- Обновление приложения
- Полезные команды
- Итоговый чеклист

**✅ devops/doc/devops-roadmap.md**
- Обновлена секция Спринта D2
- Добавлен статус "В процессе"
- Перечислены созданные файлы
- Описан ожидаемый результат

---

## Следующие шаги

### ⚠️ Требуется действие пользователя

#### Шаг 1: Открыть порты на сервере

Подключитесь к серверу:
```bash
ssh -i /Users/akozhin/projects/ai/ai-devops/systech/devops/keys/systech_admin_key root@90.156.229.75
```

Откройте порты (пример для Ubuntu с ufw):
```bash
# Проверить статус firewall
ufw status

# Открыть порты
ufw allow 3000/tcp  # Frontend
ufw allow 8000/tcp  # API

# Перезагрузить firewall
ufw reload

# Проверить
ufw status | grep -E "3000|8000"
```

Проверьте локально (с вашей машины):
```bash
nc -zv -w 3 90.156.229.75 3000
nc -zv -w 3 90.156.229.75 8000
```

Оба должны вернуть `succeeded`.

#### Шаг 2: Подготовить .env файл с реальными секретами

```bash
cd /Users/akozhin/projects/systech-aidd-live/devops
cp .env.production.example .env
nano .env  # или code .env
```

**Обязательно замените:**
- `BOT_TOKEN=your_bot_token_here`
- `LLM_API_KEY=your_api_key_here`
- `POSTGRES_PASSWORD=CHANGE_THIS_PASSWORD` (и в DATABASE_URL тоже)

**Генерация сильного пароля:**
```bash
openssl rand -base64 32
```

**Сохраните копию .env в безопасном месте!**

#### Шаг 3: Выполнить ручной деплой

Следуйте инструкции:
```bash
# Откройте в браузере или редакторе
open doc/guides/manual-deploy.md
```

**Основные команды (из инструкции):**

1. Копирование файлов на сервер:
   ```bash
   cd /Users/akozhin/projects/systech-aidd-live/devops
   
   # docker-compose.prod.yml
   scp -i /Users/akozhin/projects/ai/ai-devops/systech/devops/keys/systech_admin_key \
       docker-compose.prod.yml \
       root@90.156.229.75:/opt/systech-aidd/docker-compose.yml
   
   # .env
   scp -i /Users/akozhin/projects/ai/ai-devops/systech/devops/keys/systech_admin_key \
       .env \
       root@90.156.229.75:/opt/systech-aidd/.env
   
   # deploy-check.sh
   scp -i /Users/akozhin/projects/ai/ai-devops/systech/devops/keys/systech_admin_key \
       deploy-check.sh \
       root@90.156.229.75:/opt/systech-aidd/deploy-check.sh
   ```

2. На сервере:
   ```bash
   ssh -i /Users/akozhin/projects/ai/ai-devops/systech/devops/keys/systech_admin_key root@90.156.229.75
   
   cd /opt/systech-aidd
   
   # Загрузить образы
   docker compose pull
   
   # Запустить сервисы
   docker compose up -d
   
   # Применить миграции
   docker compose exec api alembic upgrade head
   
   # Проверить работоспособность
   ./deploy-check.sh
   ```

3. Проверка в браузере:
   - Frontend: http://90.156.229.75:3000
   - API Docs: http://90.156.229.75:8000/docs
   - API Health: http://90.156.229.75:8000/health

4. Проверка Bot в Telegram:
   - Найдите вашего бота
   - Отправьте `/start`
   - Должен ответить

---

## Созданные файлы

```
systech-aidd-live/
├── devops/
│   ├── .env.production.example      # ✅ Новый (шаблон переменных)
│   ├── docker-compose.prod.yml      # ✅ Новый (production compose)
│   ├── deploy-check.sh              # ✅ Новый (скрипт проверки)
│   ├── SPRINT_D2_STATUS.md          # ✅ Новый (этот файл)
│   └── doc/
│       └── devops-roadmap.md        # ✅ Обновлен
├── doc/
│   └── guides/
│       └── manual-deploy.md         # ✅ Новый (800+ строк инструкции)
└── .cursor/
    └── plans/
        └── sprint-d2-deploy.plan.md # ✅ План спринта
```

---

## Ключевые особенности реализации

### Безопасность

✅ **PostgreSQL изолирован:**
- Порты НЕ публикуются наружу в docker-compose.prod.yml
- Доступ только внутри Docker сети
- Для администрирования рекомендуется SSH туннель

✅ **Секреты защищены:**
- .env файл имеет права 600 (только root)
- Подробные инструкции по безопасности в manual-deploy.md
- Рекомендации по генерации сильных паролей

✅ **Firewall настроен:**
- Открыты только необходимые порты (22, 3000, 8000)
- PostgreSQL (5432) остается закрытым

### Надежность

✅ **Автоматический перезапуск:**
- Все сервисы: `restart: always`
- При падении контейнер перезапустится автоматически

✅ **Health checks:**
- PostgreSQL: pg_isready
- API: GET /health
- Frontend: GET /

✅ **Ограничение ресурсов:**
- Memory limits: 512MB
- Memory reservations: 256MB
- Защита от memory leaks

### Удобство

✅ **Готовые команды:**
- Все команды в инструкции готовы к copy-paste
- Использованы абсолютные пути к SSH ключу
- Примеры вывода для каждой команды

✅ **Автоматическая проверка:**
- Скрипт deploy-check.sh проверяет все сервисы
- Цветной вывод (красный/зеленый/желтый)
- Детальная диагностика проблем

✅ **Подробный Troubleshooting:**
- 10+ типовых проблем с решениями
- Примеры команд для диагностики
- Ссылки на документацию

---

## Следующий шаг: Спринт D3

После успешного развертывания:

**Спринт D3: Auto Deploy**
- Автоматический deploy через GitHub Actions
- SSH подключение к серверу из workflow
- Pull новых образов и restart сервисов
- Health checks и rollback при ошибках
- Notifications в Telegram/Slack
- Кнопка "Deploy" в README

---

## Полезные ссылки

- [Manual Deploy Guide](../../doc/guides/manual-deploy.md) - Пошаговая инструкция
- [Sprint D2 Plan](../../.cursor/plans/sprint-d2-deploy.plan.md) - План спринта
- [DevOps Roadmap](doc/devops-roadmap.md) - Общий план DevOps
- [Sprint D1 Complete](SPRINT_D1_COMPLETE.md) - Предыдущий спринт

---

**Текущий прогресс:** 70%  
**Готово к деплою:** ✅ Да (после открытия портов и подготовки .env)  
**Ожидается завершение:** После выполнения ручного деплоя пользователем

