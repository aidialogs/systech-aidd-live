# Sprint D1: Инструкции по тестированию

## Обзор

Все компоненты Sprint D1 созданы и готовы к тестированию. Этот документ содержит пошаговые инструкции для проверки работоспособности CI/CD pipeline.

## Предварительные требования

- [ ] Все файлы созданы и закоммичены
- [ ] У вас есть права на push в репозиторий `aidialogs/systech-aidd-live`
- [ ] У вас есть права на управление packages в организации `aidialogs`

## Тест 1: Запуск workflow при push

### Цель
Проверить что workflow запускается автоматически и образы публикуются в ghcr.io

### Шаги

1. **Закоммитить и push изменения:**
```bash
git add .
git commit -m "feat(devops): implement Sprint D1 - Build & Publish

- Add GitHub Actions workflow for automated builds
- Add docker-compose.prod.yml for registry images
- Add Makefile commands for registry operations
- Update README with badge and registry section
- Add comprehensive documentation
"
git push origin day06-smirnov-live-02-ci-pipeline
```

2. **Проверить запуск workflow:**
   - Открыть: https://github.com/aidialogs/systech-aidd-live/actions
   - Найти workflow "Build and Publish Docker Images"
   - Кликнуть на последний run

3. **Проверить параллельную сборку:**
   - В деталях run должны быть 3 job: bot, api, frontend
   - Все 3 должны выполняться параллельно
   - Все 3 должны завершиться успешно (✅)

4. **Проверить публикацию образов:**
   - Перейти на https://github.com/orgs/aidialogs/packages
   - Должны появиться 3 новых package:
     - `systech-aidd-bot`
     - `systech-aidd-api`
     - `systech-aidd-frontend`

5. **Проверить теги:**
   - Кликнуть на каждый package
   - Должны быть теги: `latest` и `sha-<commit>`

### Ожидаемый результат

- ✅ Workflow запустился автоматически после push
- ✅ Все 3 job выполнились параллельно и успешно
- ✅ Образы опубликованы в ghcr.io
- ✅ Каждый образ имеет 2 тега: latest и sha-<commit>

### В случае ошибок

Если workflow завершился с ошибкой:
1. Кликнуть на job с ошибкой
2. Развернуть failed step
3. Прочитать error message
4. Исправить проблему и повторить push

Типичные ошибки:
- **Permission denied**: проверить permissions в workflow (contents: read, packages: write)
- **Dockerfile not found**: проверить paths в matrix (dockerfile, context)
- **Login failed**: проверить что GITHUB_TOKEN доступен

## Тест 2: Проверка Pull Request

### Цель
Проверить что в PR образы собираются, но НЕ публикуются

### Шаги

1. **Создать тестовую ветку:**
```bash
git checkout -b test/workflow-pr
git commit --allow-empty -m "test: verify PR workflow"
git push origin test/workflow-pr
```

2. **Создать Pull Request:**
   - Открыть: https://github.com/aidialogs/systech-aidd-live/pulls
   - Нажать "New pull request"
   - Base: `day06-smirnov-live-02-ci-pipeline`
   - Compare: `test/workflow-pr`
   - Создать PR

3. **Проверить автоматический запуск:**
   - В PR должна появиться секция "Checks"
   - Workflow "Build and Publish Docker Images" должен запуститься

4. **Дождаться завершения:**
   - Все 3 job должны завершиться успешно

5. **Проверить что образы НЕ опубликованы:**
   - Открыть детали workflow run
   - В step "Build and push Docker image" должно быть: `push: false`
   - На https://github.com/orgs/aidialogs/packages не должно появиться новых версий

6. **Удалить тестовую ветку:**
```bash
git checkout day06-smirnov-live-02-ci-pipeline
git branch -D test/workflow-pr
git push origin --delete test/workflow-pr
```

### Ожидаемый результат

- ✅ Workflow запустился автоматически для PR
- ✅ Сборка прошла успешно
- ✅ Образы НЕ были опубликованы (push: false)
- ✅ PR показывает зеленую галочку

## Тест 3: Настройка публичного доступа

### Цель
Сделать образы публичными для использования без авторизации

### Шаги

1. **Перейти на packages:**
   - Открыть: https://github.com/orgs/aidialogs/packages

2. **Для каждого образа (bot, api, frontend):**
   
   a. **Открыть настройки:**
   - Кликнуть на package name
   - Справа нажать "Package settings"
   
   b. **Изменить visibility:**
   - Прокрутить вниз до "Danger Zone"
   - Найти "Change package visibility"
   - Нажать "Change visibility"
   - Выбрать "Public"
   - Подтвердить изменение (ввести название package)
   
   c. **Проверить статус:**
   - В верху страницы должно быть "Public" badge

3. **Проверить доступность без авторизации:**
```bash
# Убедитесь что НЕ залогинены в ghcr.io
docker logout ghcr.io

# Попробовать pull образ
docker pull ghcr.io/aidialogs/systech-aidd-bot:latest
docker pull ghcr.io/aidialogs/systech-aidd-api:latest
docker pull ghcr.io/aidialogs/systech-aidd-frontend:latest
```

### Ожидаемый результат

- ✅ Все 3 образа сделаны публичными
- ✅ `docker pull` работает без авторизации
- ✅ На странице package видно "Public" badge

## Тест 4: Локальное использование образов

### Цель
Проверить работоспособность образов из registry локально

### Шаги

1. **Подготовка окружения:**
```bash
# Остановить локальные контейнеры если запущены
make docker-down

# Проверить наличие .env файла
ls -la .env

# Если нет, создать:
cp env.docker.example .env
# Заполнить: BOT_TOKEN, LLM_API_KEY, LLM_BASE_URL, LLM_MODEL
```

2. **Скачать образы из registry:**
```bash
make docker-pull
```

**Ожидаемый вывод:**
```
Pulling images from GitHub Container Registry...
[+] Pulling ...
✔ bot Pulled
✔ api Pulled  
✔ frontend Pulled
✔ postgres Pulled (уже есть локально)
```

3. **Запустить сервисы:**
```bash
make docker-prod-up
```

**Ожидаемый вывод:**
```
Starting all services with production images from registry...
[+] Running 4/4
✔ Container systech-aidd-postgres   Started
✔ Container systech-aidd-bot        Started
✔ Container systech-aidd-api        Started
✔ Container systech-aidd-frontend   Started
```

4. **Проверить статус:**
```bash
make docker-prod-ps
```

**Ожидаемый вывод:**
Все 4 контейнера в статусе "Up"

5. **Применить миграции (только при первом запуске):**
```bash
docker compose -f docker-compose.prod.yml exec api uv run alembic upgrade head
```

6. **Проверить логи:**
```bash
make docker-prod-logs
```

**Проверить:**
- Bot успешно запустился и подключился к БД
- API запустился на порту 8000
- Frontend запустился на порту 3000
- Нет критических ошибок

7. **Проверить endpoints:**
```bash
# Health check
curl http://localhost:8000/health

# API docs
open http://localhost:8000/docs

# Frontend
open http://localhost:3000
```

8. **Проверить Telegram bot:**
   - Отправить сообщение боту в Telegram
   - Получить ответ от LLM
   - Проверить что контекст сохраняется

9. **Проверить логи конкретного сервиса:**
```bash
docker compose -f docker-compose.prod.yml logs bot
docker compose -f docker-compose.prod.yml logs api
docker compose -f docker-compose.prod.yml logs frontend
```

10. **Остановить сервисы:**
```bash
make docker-prod-down
```

### Ожидаемый результат

- ✅ Образы успешно скачались из registry
- ✅ Все 4 сервиса запустились
- ✅ Миграции применились без ошибок
- ✅ API доступен и отвечает на запросы
- ✅ Frontend доступен в браузере
- ✅ Bot отвечает на сообщения в Telegram
- ✅ В логах нет критических ошибок

## Тест 5: Проверка Badge в README

### Цель
Убедиться что badge отображается корректно

### Шаги

1. **Открыть README на GitHub:**
   - https://github.com/aidialogs/systech-aidd-live/blob/day06-smirnov-live-02-ci-pipeline/README.md

2. **Проверить badge:**
   - После заголовка должен быть badge "Build and Publish"
   - Badge должен быть зеленым с текстом "passing"

3. **Кликнуть на badge:**
   - Должен открыться список workflow runs
   - https://github.com/aidialogs/systech-aidd-live/actions/workflows/build-and-publish.yml

### Ожидаемый результат

- ✅ Badge отображается корректно
- ✅ Badge показывает статус "passing" (зеленый)
- ✅ Клик на badge ведет на GitHub Actions

## Тест 6: Ручной запуск workflow

### Цель
Проверить workflow_dispatch (ручной запуск)

### Шаги

1. **Перейти на Actions:**
   - https://github.com/aidialogs/systech-aidd-live/actions

2. **Выбрать workflow:**
   - Кликнуть на "Build and Publish Docker Images"

3. **Запустить вручную:**
   - Нажать "Run workflow" (справа)
   - Выбрать ветку: `day06-smirnov-live-02-ci-pipeline`
   - Нажать зеленую кнопку "Run workflow"

4. **Дождаться завершения:**
   - Workflow должен запуститься
   - Все 3 job должны завершиться успешно

### Ожидаемый результат

- ✅ Workflow можно запустить вручную
- ✅ Сборка и публикация проходят успешно

## Тест 7: Проверка версионирования

### Цель
Убедиться что образы тегируются правильно

### Шаги

1. **Получить commit hash:**
```bash
git log -1 --format=%H
# Скопировать первые 7 символов (короткий SHA)
```

2. **Проверить наличие тегов:**
   - Открыть: https://github.com/orgs/aidialogs/packages/container/systech-aidd-bot
   - В списке версий должны быть:
     - `latest`
     - `sha-<SHORT_SHA>` (7 символов)

3. **Pull конкретной версии:**
```bash
# Заменить SHORT_SHA на реальный
docker pull ghcr.io/aidialogs/systech-aidd-bot:sha-<SHORT_SHA>
```

4. **Сравнить образы:**
```bash
docker images | grep systech-aidd-bot
```

### Ожидаемый результат

- ✅ Образ имеет теги `latest` и `sha-<commit>`
- ✅ Можно pull конкретную версию по SHA
- ✅ SHA тег соответствует commit hash

## Итоговая проверка

### Чеклист готовности

Отметьте все пункты после успешного тестирования:

- [ ] Тест 1: Workflow запускается при push ✅
- [ ] Тест 2: Workflow работает в PR (без публикации) ✅
- [ ] Тест 3: Образы сделаны публичными ✅
- [ ] Тест 4: Образы работают локально ✅
- [ ] Тест 5: Badge отображается корректно ✅
- [ ] Тест 6: Ручной запуск работает ✅
- [ ] Тест 7: Версионирование работает ✅

### Если все тесты прошли успешно

**Поздравляем! Sprint D1 успешно завершен!** 🎉

Следующий шаг: Sprint D2 - Развертывание на сервер

### Если есть проблемы

1. Проверить логи workflow run
2. Проверить настройки репозитория (permissions)
3. Проверить содержимое файлов
4. Обратиться к документации:
   - `/devops/doc/guides/github-actions-intro.md`
   - `/devops/doc/plans/sprint-d1-build-publish.md`

## Полезные команды

### Просмотр образов
```bash
# Список локальных образов
docker images | grep systech-aidd

# Информация об образе
docker inspect ghcr.io/aidialogs/systech-aidd-bot:latest

# История layers
docker history ghcr.io/aidialogs/systech-aidd-bot:latest
```

### Отладка
```bash
# Логи контейнера
docker compose -f docker-compose.prod.yml logs -f bot

# Exec в контейнер
docker compose -f docker-compose.prod.yml exec api bash

# Проверка переменных окружения
docker compose -f docker-compose.prod.yml exec api env | grep DATABASE_URL
```

### Очистка
```bash
# Остановить prod окружение
make docker-prod-down

# Удалить локальные образы
docker rmi ghcr.io/aidialogs/systech-aidd-bot:latest
docker rmi ghcr.io/aidialogs/systech-aidd-api:latest
docker rmi ghcr.io/aidialogs/systech-aidd-frontend:latest

# Очистка всего
docker system prune -a
```

## Контакты

Если возникли вопросы или проблемы:
1. Проверить документацию в `/devops/doc/`
2. Проверить Issues на GitHub
3. Обратиться к команде DevOps

