# Следующие шаги для завершения Спринта D2

## ✅ Что уже готово

Созданы все необходимые файлы для развертывания:

1. **devops/.env.production.example** (6.4 KB)
   - Шаблон всех переменных окружения
   - Подробные комментарии на русском
   - Рекомендации по безопасности
   - Checklist перед деплоем

2. **devops/docker-compose.prod.yml** (6.5 KB)
   - Production конфигурация
   - Образы из `ghcr.io/aidialogs/systech-aidd-live`
   - PostgreSQL изолирован (порты не открыты)
   - Health checks для всех сервисов
   - Memory limits

3. **devops/deploy-check.sh** (9.4 KB, исполняемый)
   - Автоматическая проверка всех сервисов
   - Цветной вывод (красный/зеленый)
   - Диагностика проблем

4. **doc/guides/manual-deploy.md** (1185 строк)
   - Полная пошаговая инструкция
   - Все команды ready-to-copy
   - 10+ troubleshooting scenarios
   - Управление сервисами

5. **devops/doc/devops-roadmap.md** - обновлен
6. **devops/SPRINT_D2_STATUS.md** - статус спринта

---

## ⚠️ Что нужно сделать (требуется ваше участие)

### Шаг 1: Проверить доступность сервера

```bash
# Попробуйте подключиться к серверу
ssh -i /Users/akozhin/projects/ai/ai-devops/systech/devops/keys/systech_admin_key root@90.156.229.75

# Если подключение не работает - проверьте:
# - Сервер включен
# - Сеть работает
# - SSH ключ правильный
```

### Шаг 2: Открыть порты на сервере

После подключения к серверу:

```bash
# Проверить firewall
ufw status

# Открыть порты (если нужно)
ufw allow 3000/tcp  # Frontend
ufw allow 8000/tcp  # API

# Перезагрузить firewall
ufw reload

# Проверить
ufw status | grep -E "3000|8000"
```

**Ожидаемый результат:**
```
3000/tcp                   ALLOW       Anywhere
8000/tcp                   ALLOW       Anywhere
```

**Проверить с локальной машины:**
```bash
nc -zv -w 3 90.156.229.75 3000
nc -zv -w 3 90.156.229.75 8000
```

Оба должны вернуть `succeeded`.

### Шаг 3: Подготовить .env файл с реальными секретами

```bash
cd /Users/akozhin/projects/systech-aidd-live/devops

# Скопировать шаблон
cp .env.production.example .env

# Редактировать
nano .env  # или: code .env
```

**Обязательно замените:**
```bash
BOT_TOKEN=your_bot_token_here               → ваш реальный токен от @BotFather
LLM_API_KEY=your_api_key_here               → ваш реальный API ключ
POSTGRES_PASSWORD=CHANGE_THIS_PASSWORD      → сильный пароль (16+ символов)
# И тот же пароль в DATABASE_URL:
DATABASE_URL=postgresql+asyncpg://systech_user:ВАШ_ПАРОЛЬ@postgres:5432/systech_aidd
```

**Генерация сильного пароля:**
```bash
openssl rand -base64 32
```

**⚠️ ВАЖНО:** Сохраните копию .env в безопасном месте (password manager)!

### Шаг 4: Выполнить ручной деплой

**Следуйте подробной инструкции:**
```bash
open doc/guides/manual-deploy.md
# или
cat doc/guides/manual-deploy.md
```

**Краткая версия (полная в manual-deploy.md):**

#### 4.1. Создать директорию на сервере

```bash
ssh -i /Users/akozhin/projects/ai/ai-devops/systech/devops/keys/systech_admin_key root@90.156.229.75

# На сервере:
mkdir -p /opt/systech-aidd
cd /opt/systech-aidd
```

#### 4.2. Скопировать файлы (с локальной машины)

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

#### 4.3. Развернуть на сервере

```bash
# На сервере (в SSH сессии)
cd /opt/systech-aidd

# Установить права на .env
chmod 600 .env

# Загрузить образы
docker compose pull

# Запустить сервисы
docker compose up -d

# Применить миграции
docker compose exec api alembic upgrade head

# Проверить работоспособность
chmod +x deploy-check.sh
./deploy-check.sh
```

### Шаг 5: Проверить работоспособность

**В браузере:**
- Frontend: http://90.156.229.75:3000
- API Docs: http://90.156.229.75:8000/docs
- API Health: http://90.156.229.75:8000/health

**В Telegram:**
- Найдите вашего бота
- Отправьте `/start`
- Должен ответить

**На сервере:**
```bash
docker compose ps        # Все должны быть Up
docker compose logs -f   # Проверить логи
```

---

## 📋 Чеклист завершения

После выполнения всех шагов убедитесь:

- [ ] Порты 3000 и 8000 открыты на сервере
- [ ] Все 4 контейнера запущены (postgres, bot, api, frontend)
- [ ] PostgreSQL health check проходит
- [ ] API доступен: http://90.156.229.75:8000/docs
- [ ] Frontend доступен: http://90.156.229.75:3000
- [ ] Bot отвечает в Telegram на `/start`
- [ ] Миграции БД применены
- [ ] Логи без критичных ошибок
- [ ] .env файл защищен (chmod 600) на сервере
- [ ] Создан бэкап .env в безопасном месте

---

## 🆘 Если что-то не работает

**См. раздел Troubleshooting в manual-deploy.md:**
- Контейнер не запускается (Exited)
- API недоступен (Connection refused)
- Frontend не загружается
- Bot не отвечает в Telegram
- PostgreSQL недоступен
- Ошибка миграций Alembic
- Образы не загружаются (unauthorized)
- Недостаточно места на диске
- Порты заняты
- И другие...

**Или запустите диагностику:**
```bash
# На сервере
cd /opt/systech-aidd
./deploy-check.sh
```

---

## 📞 Получить помощь

Если возникли проблемы:

1. **Проверьте логи:**
   ```bash
   docker compose logs -f api
   docker compose logs -f bot
   ```

2. **Проверьте статус:**
   ```bash
   docker compose ps
   ```

3. **Запустите deploy-check.sh:**
   ```bash
   ./deploy-check.sh
   ```

4. **Обратитесь к manual-deploy.md** - там 1185 строк подробной документации!

---

## 🎯 После успешного деплоя

Когда всё заработает, сообщите мне и я:

1. Создам `SPRINT_D2_COMPLETE.md` с полным отчетом
2. Обновлю devops-roadmap.md со статусом ✅
3. Подготовлю план для **Спринта D3: Auto Deploy**

---

**Удачи с развертыванием! 🚀**

Все инструкции готовы, файлы подготовлены - осталось только выполнить команды.

