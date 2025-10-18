# Инструкция по тестированию CI Workflow

Этот документ описывает шаги для тестирования GitHub Actions workflow после создания.

---

## Предварительные требования

1. Репозиторий должен быть в GitHub
2. Настроены Workflow permissions (см. [GUIDE-10](../doc/guides/10-ci-cd-guide.md#настройка-github))
3. Все файлы из Sprint D2 закоммичены

---

## Шаг 1: Локальная проверка

Перед push в GitHub, проверьте что всё работает локально:

```bash
# 1. Backend lint
make ci-lint-backend
# Ожидается: ✅ Backend lint passed

# 2. Frontend lint (если есть Node.js и pnpm)
make ci-lint-frontend
# Ожидается: ✅ Frontend lint passed

# 3. Tests
make ci-test
# Ожидается: ✅ Tests passed

# 4. Docker builds (опционально, требует время)
make ci-build
# Ожидается: ✅ All images built successfully
```

**Если всё прошло успешно локально - можно пушить в GitHub.**

---

## Шаг 2: Создание тестовой ветки

```bash
# Создать новую ветку для тестирования
git checkout -b test-ci-pipeline

# Сделать небольшое изменение (для триггера workflow)
echo "" >> README.md

# Закоммитить изменения
git add .
git commit -m "test: verify CI pipeline works"

# Запушить в GitHub
git push -u origin test-ci-pipeline
```

---

## Шаг 3: Проверка workflow в GitHub

1. **Открыть GitHub Actions:**
   - Перейти: https://github.com/YOUR_USERNAME/systech-aidd-live/actions
   - Должен появиться новый workflow run "CI Pipeline"

2. **Проверить статус jobs:**
   - Кликнуть на workflow run
   - Видеть 6 jobs:
     - ✅ lint-backend
     - ✅ lint-frontend
     - ✅ test
     - ✅ build-images (bot, api, frontend - 3 параллельных)
     - ⏭️ security-scan (пропущен, т.к. не main)
     - ⏭️ publish (пропущен, т.к. не main)

3. **Проверить логи каждого job:**
   - Кликнуть на job name
   - Просмотреть steps
   - Убедиться что нет ошибок

**Ожидаемое время:** ~4-5 минут для первого запуска

---

## Шаг 4: Создание Pull Request

```bash
# Открыть PR через GitHub UI или gh CLI:
gh pr create --title "test: CI pipeline" --body "Testing CI workflow"

# Или через веб-интерфейс:
# https://github.com/YOUR_USERNAME/systech-aidd-live/compare/test-ci-pipeline
```

**Проверить:**
1. В PR автоматически появляются checks
2. Все checks должны пройти успешно (зелёные галочки)
3. Можно просмотреть детали каждого check

---

## Шаг 5: Merge в main

```bash
# Через веб-интерфейс нажать "Merge pull request"
# Или через CLI:
gh pr merge --squash

# Переключиться на main и pull
git checkout main
git pull origin main
```

**После merge в main:**

1. **Новый workflow run запустится автоматически**
2. **На этот раз выполнятся ВСЕ jobs:**
   - ✅ lint-backend
   - ✅ lint-frontend
   - ✅ test
   - ✅ build-images (3 образа)
   - ✅ security-scan (3 образа) - **только на main**
   - ✅ publish (3 образа) - **только на main**

3. **Время выполнения:** ~7-8 минут

---

## Шаг 6: Проверка опубликованных образов

После успешного выполнения publish job:

1. **Перейти в GitHub Packages:**
   - https://github.com/YOUR_USERNAME?tab=packages
   - Или https://github.com/YOUR_USERNAME/systech-aidd-live/pkgs

2. **Проверить что опубликованы 3 образа:**
   - `systech-aidd-live-bot`
   - `systech-aidd-live-api`
   - `systech-aidd-live-frontend`

3. **Проверить tags каждого образа:**
   - `latest`
   - `branch-main`
   - `sha-XXXXXXX` (где XXXXXXX - короткий SHA коммита)

4. **Опционально: Pull образ локально:**
   ```bash
   # Для публичных образов:
   docker pull ghcr.io/YOUR_USERNAME/systech-aidd-live-bot:latest
   
   # Для приватных образов сначала login:
   echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_USERNAME --password-stdin
   docker pull ghcr.io/YOUR_USERNAME/systech-aidd-live-bot:latest
   ```

---

## Шаг 7: Проверка Security Scan

1. **Перейти в Security tab:**
   - https://github.com/YOUR_USERNAME/systech-aidd-live/security

2. **Открыть Code scanning:**
   - Security → Code scanning
   - Должны быть видны результаты Trivy сканирования

3. **Проверить найденные уязвимости:**
   - Видеть отдельные отчеты для bot, api, frontend
   - Видеть severity (HIGH, CRITICAL)
   - Можно dismiss false positives

---

## Troubleshooting

### Workflow не запускается

**Проверить:**
1. Actions включены: Settings → Actions → General → "Allow all actions"
2. Синтаксис YAML корректен: https://www.yamllint.com/
3. Branch указан в triggers (main, develop)

**Решение:**
```bash
# Пересоздать ветку с изменением
git checkout -b test-ci-v2
echo "test" >> README.md
git add . && git commit -m "test: trigger workflow"
git push -u origin test-ci-v2
```

### lint-backend fails

**Ошибки:**
```
Error: Process completed with exit code 1
```

**Решение:**
```bash
# Запустить локально
make ci-lint-backend

# Посмотреть детали
uv run ruff check src/ tests/
uv run mypy src/ tests/

# Исправить ошибки
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/
```

### build-images fails

**Ошибки:**
```
ERROR: failed to solve: process timeout
```

**Решение:**
```bash
# 1. Проверить .dockerignore
cat .dockerignore
# Убедиться что node_modules/, .git/ исключены

# 2. Проверить Dockerfile локально
docker build -f devops/Dockerfile.bot -t test .

# 3. Очистить GitHub Actions cache
# GitHub → Actions → Caches → Delete all caches
```

### publish fails - permission denied

**Ошибки:**
```
Error: denied: permission_denied
```

**Решение:**
```bash
# Проверить permissions в ci.yml:
permissions:
  contents: read
  packages: write  # Должно быть!

# Проверить Settings:
# Settings → Actions → General → Workflow permissions
# ☑ Read and write permissions
```

---

## Успешное завершение

После всех шагов вы должны видеть:

✅ Workflow запускается на каждом push/PR  
✅ Все lint checks проходят  
✅ Tests выполняются с coverage  
✅ Docker образы собираются успешно  
✅ Security scan выполняется на main  
✅ Образы публикуются в ghcr.io  
✅ Результаты видны в GitHub UI  

**Поздравляю! CI Pipeline работает! 🎉**

---

## Следующие шаги

1. **Настроить Branch Protection:**
   - Settings → Branches → Add rule
   - Require status checks: lint-backend, lint-frontend, test, build-images

2. **Добавить CI badge в README:**
   ```markdown
   [![CI](https://github.com/YOUR_USERNAME/systech-aidd-live/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/systech-aidd-live/actions/workflows/ci.yml)
   ```
   (Замените YOUR_USERNAME на ваше имя пользователя)

3. **Сделать образы публичными (опционально):**
   - GitHub → Packages → выбрать образ
   - Package settings → Change visibility → Public

4. **Начать Sprint D3:** CD Pipeline & Deployment

---

## Полезные ссылки

- [GUIDE-10: CI/CD Pipeline](../doc/guides/10-ci-cd-guide.md)
- [ADR-09: CI/CD Architecture](../doc/adrs/ADR-09.md)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Container Registry](https://docs.github.com/en/packages)

---

**Версия:** 1.0  
**Дата:** 2025-10-17

