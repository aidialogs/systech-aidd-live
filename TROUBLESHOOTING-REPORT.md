# Troubleshooting Report - Sprint S4

## Дата: 17 октября 2025

## Проблемы и решения

### Проблема 1: Dashboard показывает Mock данные

**Симптомы:**
- Dashboard показывает фейковые ровные числа (11930, 411, 387)

**Причина:**
- В `.env` отсутствовала переменная `STAT_COLLECTOR_MODE`
- По умолчанию использовался режим "mock"

**Решение:**
```bash
# Добавлено в .env:
STAT_COLLECTOR_MODE=real
```

**Результат:** ✅ Dashboard теперь показывает реальные данные из PostgreSQL

---

### Проблема 2: Chat API возвращает ошибку

**Симптомы:**
- POST `/api/v1/chat/message` возвращает: "Извините, произошла ошибка"
- В логах: `ConnectionRefusedError: [Errno 61] Connection refused`

**Причина:**
- PostgreSQL контейнер был остановлен
- API запущен когда БД не была доступна

**Решение:**
```bash
# Запустить PostgreSQL
docker start systech-aidd-postgres

# Перезапустить API
pkill -f "python.*api_server"
uv run python -m src.api_server
```

**Результат:** ✅ Chat API работает

---

### Проблема 3: Admin режим отклоняет валидные SELECT запросы

**Симптомы:**
- Admin mode генерирует правильный SQL
- Но возвращает: "Разрешены только SELECT запросы"
- SQL: `SELECT COUNT(*) FROM messages WHERE is_deleted = false;`

**Причина:**
- Валидация `_is_safe_sql()` искала подстроку "DELETE"
- Находила "DELETE" внутри слова "is_**delete**d"

**Решение:**
```python
# Исправлена валидация для поиска целых слов:
import re
for keyword in dangerous_keywords:
    if re.search(r'\b' + keyword + r'\b', sql_upper):
        return False
```

**Результат:** ✅ Admin режим работает с text2sql

---

## Текущий статус

### ✅ Что работает:

1. **Backend API (Real mode)**
   - RealStatCollector с SQL запросами к PostgreSQL
   - Chat API с normal режимом
   - Chat API с admin режимом (text2sql)
   - История сообщений сохраняется в БД

2. **Dashboard**
   - Показывает реальные данные из БД:
     - 12 сообщений
     - 2 пользователя
     - 2 чата
     - Графики по реальным данным

3. **Chat**
   - Normal режим: общение с LLM работает
   - Admin режим: text2sql pipeline работает
   - Пример:
     - Вопрос: "Сколько всего сообщений?"
     - SQL: `SELECT COUNT(*) FROM messages;`
     - Ответ: "Всего в базе данных 12 сообщений."

### 📦 Конфигурация

#### .env файл:
```bash
BOT_TOKEN=...
LLM_API_KEY=...
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openai/gpt-oss-20b:free
DATABASE_URL=postgresql+asyncpg://systech_user:systech_password@localhost:5432/systech_aidd

# ДОБАВЛЕНО:
STAT_COLLECTOR_MODE=real
API_HOST=0.0.0.0
API_PORT=8000
```

#### PostgreSQL:
```bash
# Запущен в Docker
docker ps | grep systech-aidd-postgres
# Должен показать: Up X seconds

# Если остановлен:
docker start systech-aidd-postgres
```

#### API Server:
```bash
# Запуск
uv run python -m src.api_server

# Проверка
curl http://localhost:8000/health
```

---

## Тестирование

### Test 1: Health check
```bash
curl http://localhost:8000/health
# Ожидается: {"status": "ok"}
```

### Test 2: Statistics (Dashboard)
```bash
curl "http://localhost:8000/api/v1/statistics?period=all" | python3 -m json.tool
# Должно показывать реальные данные из БД
```

### Test 3: Chat (Normal mode)
```bash
curl -X POST "http://localhost:8000/api/v1/chat/message" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "mode": "normal", "user_id": 1, "chat_id": 1}' \
  | python3 -m json.tool
# Должен вернуть ответ от LLM
```

### Test 4: Chat (Admin mode)
```bash
curl -X POST "http://localhost:8000/api/v1/chat/message" \
  -H "Content-Type: application/json" \
  -d '{"message": "Сколько сообщений?", "mode": "admin", "user_id": 1, "chat_id": 1}' \
  | python3 -m json.tool
# Должен вернуть SQL и ответ на основе данных
```

---

## Исправленные файлы

1. **/.env** - добавлены переменные `STAT_COLLECTOR_MODE`, `API_HOST`, `API_PORT`
2. **/src/api/chat_handler.py** - исправлена валидация SQL (word boundaries)

---

## Чек-лист перед запуском

- [ ] PostgreSQL запущен: `docker ps | grep systech-aidd-postgres`
- [ ] `.env` содержит `STAT_COLLECTOR_MODE=real`
- [ ] API сервер запущен: `curl http://localhost:8000/health`
- [ ] Frontend запущен (если нужен): `cd frontend && pnpm dev`

---

## Следующие шаги

1. ✅ Backend работает
2. ✅ Dashboard показывает реальные данные
3. ✅ Chat работает (normal + admin)
4. 🔄 Нужно проверить Frontend интеграцию

---

## Полезные команды

```bash
# Остановить все
pkill -f "python.*api_server"
docker stop systech-aidd-postgres

# Запустить все
docker start systech-aidd-postgres
sleep 3
cd /path/to/project
uv run python -m src.api_server > api_server.log 2>&1 &

# Проверить логи
tail -f api_server.log

# Тесты через Makefile
make chat-test           # Normal mode
make chat-test-admin     # Admin mode
make api-test            # Statistics
```

---

**Статус:** ✅ Все основные функции работают!



