# Работа с CICD веткой

## 🎯 Назначение

Ветка `cicd` используется для:
- Тестирования публикации Docker образов в ghcr.io
- Проверки деплоя на сервере БЕЗ влияния на main
- Экспериментов с CI/CD процессом

**Преимущество:** Полный CI/CD pipeline (включая publish) без риска для production.

---

## 📋 Что работает в CICD ветке

При push в `cicd` ветку выполняются **ВСЕ** jobs:

| Job | Описание | Время |
|-----|----------|-------|
| ✅ lint-backend | Ruff + MyPy | ~40s |
| ✅ lint-frontend | ESLint + TypeScript | ~45s |
| ✅ test | Pytest с coverage | ~30s |
| ✅ build-images | Docker сборка (3 образа) | ~2-3min |
| ✅ **security-scan** | Trivy сканирование | ~1-2min |
| ✅ **publish** | Публикация в ghcr.io | ~2-3min |

---

## 🚀 Как работать с CICD веткой

### Вариант 1: Прямой push в cicd

**Для быстрых тестов изменений:**

```bash
# Переключиться на cicd
git checkout cicd

# Внести изменения
# ... редактирование файлов ...

# Закоммитить
git add .
git commit -m "test: описание изменений"

# Запушить - workflow запустится автоматически
git push
```

**Результат:**
- ✅ Workflow запустится сразу
- ✅ Образы опубликуются в ghcr.io с тегом `branch-cicd`
- ✅ Можно сразу тестировать на сервере

---

### Вариант 2: Merge другой ветки в cicd

**Для тестирования фич перед merge в main:**

```bash
# У вас есть feature ветка (например, day6-cicd-draft)
git checkout day6-cicd-draft

# Убедиться что все закоммичено
git status

# Переключиться на cicd
git checkout cicd

# Смержить feature ветку
git merge day6-cicd-draft

# Разрешить конфликты если есть
# ... исправление конфликтов ...
# git add .
# git commit

# Запушить - workflow запустится
git push
```

**Результат:**
- ✅ Все изменения из feature ветки попадают в cicd
- ✅ Полный CI/CD pipeline
- ✅ Образы с последними изменениями

---

### Вариант 3: Pull Request в cicd

**Для code review перед тестированием:**

```bash
# Создать PR в cicd ветку
gh pr create --base cicd --head day6-cicd-draft \
  --title "test: merge for CICD testing" \
  --body "Testing changes before production merge"

# Или через веб-интерфейс:
# https://github.com/aidialogs/systech-aidd-live/compare/cicd...day6-cicd-draft
```

**После review и merge:**
- ✅ Workflow запустится автоматически
- ✅ Образы опубликуются

---

## 📦 Опубликованные образы

После успешного publish образы доступны по адресам:

```bash
# Bot
ghcr.io/aidialogs/systech-aidd-live-bot:branch-cicd
ghcr.io/aidialogs/systech-aidd-live-bot:sha-XXXXXXX

# API
ghcr.io/aidialogs/systech-aidd-live-api:branch-cicd
ghcr.io/aidialogs/systech-aidd-live-api:sha-XXXXXXX

# Frontend
ghcr.io/aidialogs/systech-aidd-live-frontend:branch-cicd
ghcr.io/aidialogs/systech-aidd-live-frontend:sha-XXXXXXX
```

---

## 🖥️ Тестирование на сервере

### Pull образов с cicd ветки

```bash
# На сервере: Login в ghcr.io
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pull образов с тегом branch-cicd
docker pull ghcr.io/aidialogs/systech-aidd-live-bot:branch-cicd
docker pull ghcr.io/aidialogs/systech-aidd-live-api:branch-cicd
docker pull ghcr.io/aidialogs/systech-aidd-live-frontend:branch-cicd

# Или использовать конкретный SHA
docker pull ghcr.io/aidialogs/systech-aidd-live-bot:sha-abc123
```

### Запуск через docker-compose

Создайте `docker-compose.cicd.yml` на сервере:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: systech_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: systech_aidd
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  bot:
    image: ghcr.io/aidialogs/systech-aidd-live-bot:branch-cicd
    environment:
      BOT_TOKEN: ${BOT_TOKEN}
      LLM_API_KEY: ${LLM_API_KEY}
      LLM_BASE_URL: ${LLM_BASE_URL}
      LLM_MODEL: ${LLM_MODEL}
      DATABASE_URL: postgresql+asyncpg://systech_user:${DB_PASSWORD}@postgres:5432/systech_aidd
    depends_on:
      - postgres
    restart: unless-stopped

  api:
    image: ghcr.io/aidialogs/systech-aidd-live-api:branch-cicd
    environment:
      DATABASE_URL: postgresql+asyncpg://systech_user:${DB_PASSWORD}@postgres:5432/systech_aidd
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    restart: unless-stopped

  frontend:
    image: ghcr.io/aidialogs/systech-aidd-live-frontend:branch-cicd
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://api:8000
    depends_on:
      - api
    restart: unless-stopped

volumes:
  postgres_data:
```

**Запуск:**

```bash
# Создать .env файл
cat > .env << EOF
DB_PASSWORD=your_secure_password
BOT_TOKEN=your_bot_token
LLM_API_KEY=your_llm_key
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=anthropic/claude-3.5-sonnet
EOF

# Запустить
docker-compose -f docker-compose.cicd.yml up -d

# Проверить статус
docker-compose -f docker-compose.cicd.yml ps

# Просмотр логов
docker-compose -f docker-compose.cicd.yml logs -f
```

---

## 🔄 Обновление на сервере

Когда запушили новые изменения в cicd:

```bash
# На сервере: остановить сервисы
docker-compose -f docker-compose.cicd.yml down

# Pull обновленные образы
docker-compose -f docker-compose.cicd.yml pull

# Запустить обновленные
docker-compose -f docker-compose.cicd.yml up -d

# Проверить что всё работает
docker-compose -f docker-compose.cicd.yml ps
docker-compose -f docker-compose.cicd.yml logs bot
```

**Или одной командой:**

```bash
docker-compose -f docker-compose.cicd.yml up -d --pull always
```

---

## 📊 Мониторинг

### Проверка работы сервисов

```bash
# Health checks
curl http://localhost:8000/health
curl http://localhost:3000

# Логи в реальном времени
docker-compose -f docker-compose.cicd.yml logs -f bot
docker-compose -f docker-compose.cicd.yml logs -f api

# Статус контейнеров
docker ps
```

### Просмотр опубликованных образов

GitHub Packages:
```
https://github.com/orgs/aidialogs/packages
```

---

## 🔧 Troubleshooting

### Образы не публикуются

**Проверить:**
1. Workflow завершился успешно: https://github.com/aidialogs/systech-aidd-live/actions
2. Job `publish` выполнился (не пропущен)
3. Нет ошибок authentication в логах

**Решение:**
```bash
# Проверить что вы в cicd ветке
git branch

# Проверить workflow файл
cat .github/workflows/ci.yml | grep -A5 "publish:"
```

### Не могу pull образы на сервере

**Проверить:**
1. Образы приватные или публичные
2. GITHUB_TOKEN актуален

**Для приватных образов:**
```bash
# Создать Personal Access Token с правом read:packages
# Settings → Developer settings → Personal access tokens
# Scopes: read:packages

# Login на сервере
echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_USERNAME --password-stdin
```

### Конфликты при merge

```bash
# Посмотреть конфликтующие файлы
git status

# Открыть файлы и разрешить конфликты
# Удалить маркеры <<<<<<, ======, >>>>>>

# Закоммитить
git add .
git commit -m "resolve: merge conflicts"
git push
```

---

## ✅ Checklist: Полный цикл тестирования

- [ ] Push изменений в cicd ветку
- [ ] Дождаться завершения workflow (~7-8 минут)
- [ ] Проверить что publish job успешен
- [ ] Проверить образы в GitHub Packages
- [ ] На сервере: pull обновленных образов
- [ ] Запустить docker-compose
- [ ] Проверить health checks
- [ ] Тестировать функционал
- [ ] Если всё OK → можно мерджить в main

---

## 🎓 Best Practices

1. **Используйте осмысленные commit messages:**
   ```bash
   git commit -m "test(bot): проверка новой фичи"
   git commit -m "fix(api): исправление endpoint"
   ```

2. **Проверяйте workflow перед тестированием на сервере:**
   - GitHub Actions должен завершиться успешно
   - Все checks зелёные

3. **Тегируйте важные версии:**
   ```bash
   git tag -a v0.1.0-cicd -m "Testing version 0.1.0"
   git push origin v0.1.0-cicd
   ```

4. **Логируйте результаты тестирования:**
   - Что тестировали
   - Что работает
   - Что нужно исправить

---

## 📝 Примеры workflow

### Пример 1: Быстрая проверка фикса

```bash
# Есть bug в bot
git checkout cicd
git pull

# Исправить bug
vim src/bot_handler.py

# Коммит и push
git add .
git commit -m "fix(bot): исправление обработки команды /reset"
git push

# Ждать ~8 минут
# Тестировать на сервере
# Если OK - мерджить в main
```

### Пример 2: Тестирование большой фичи

```bash
# Разработка в feature ветке
git checkout -b feature/new-dashboard
# ... разработка ...
git add . && git commit -m "feat: new dashboard"
git push -u origin feature/new-dashboard

# Тестирование через cicd
git checkout cicd
git merge feature/new-dashboard
git push

# После теста на сервере
git checkout main
git merge feature/new-dashboard
git push
```

---

## 🔗 Полезные ссылки

- **GitHub Actions:** https://github.com/aidialogs/systech-aidd-live/actions
- **GitHub Packages:** https://github.com/orgs/aidialogs/packages
- **CI/CD Guide:** [doc/guides/10-ci-cd-guide.md](../doc/guides/10-ci-cd-guide.md)
- **Docker Deployment:** [doc/guides/09-docker-deployment.md](../doc/guides/09-docker-deployment.md)

---

**Версия:** 1.0  
**Дата:** 2025-10-17  
**Автор:** DevOps Team

