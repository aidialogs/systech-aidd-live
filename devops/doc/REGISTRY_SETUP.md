# Настройка GitHub Container Registry

## Обзор

GitHub Container Registry (ghcr.io) — это Docker registry от GitHub для хранения и распространения Docker образов. По умолчанию все образы создаются как **приватные** и требуют аутентификацию для скачивания.

Для упрощения использования образов в спринтах D2 (ручной deploy) и D3 (авто deploy) рекомендуется сделать образы **публичными**.

## Автоматическая публикация образов

Образы автоматически публикуются в ghcr.io через GitHub Actions workflow (`.github/workflows/build.yml`) при каждом push в ветку `day6-ci-draft`.

**Что происходит автоматически:**

1. GitHub Actions собирает Docker образы для bot, api, frontend
2. Аутентифицируется в ghcr.io через `GITHUB_TOKEN`
3. Публикует образы с тегами:
   - `latest` — последняя версия
   - `sha-abc1234` — конкретный коммит (короткий SHA)

**Где находятся образы:**

После первой публикации образы появляются в GitHub Packages:
- `ghcr.io/<owner>/<repo>/bot:latest`
- `ghcr.io/<owner>/<repo>/api:latest`
- `ghcr.io/<owner>/<repo>/frontend:latest`

Пример: `ghcr.io/akozhin/systech-aidd-live/bot:latest`

## Сделать образы публичными

### Зачем делать образы публичными?

**Приватные образы** (по умолчанию):
- ❌ Требуют `docker login ghcr.io` перед pull
- ❌ Нужен Personal Access Token с правами на чтение packages
- ❌ Неудобно для быстрого тестирования

**Публичные образы**:
- ✅ Скачиваются без авторизации: `docker pull ghcr.io/user/repo/bot:latest`
- ✅ Удобны для CI/CD и автоматического развертывания
- ✅ Подходят для open-source проектов

### Пошаговая инструкция

#### Шаг 1: Перейти в GitHub Packages

1. Откройте репозиторий на GitHub
2. Перейдите в раздел **Packages** (справа на главной странице репозитория)
   - Или прямая ссылка: `https://github.com/<owner>/<repo>/packages`

#### Шаг 2: Выбрать образ

Вы увидите список опубликованных образов:
- `bot`
- `api`
- `frontend`

Кликните на каждый образ по очереди.

#### Шаг 3: Изменить видимость

Для каждого образа:

1. Нажмите **"Package settings"** (справа сверху)
2. Прокрутите вниз до секции **"Danger Zone"**
3. Найдите **"Change package visibility"**
4. Нажмите **"Change visibility"**
5. Выберите **"Public"**
6. Подтвердите действие, введя имя пакета

**Важно:** Повторите это для всех трех образов (bot, api, frontend).

#### Шаг 4: Проверка

После изменения видимости проверьте, что образы доступны без авторизации:

```bash
# Должно работать без docker login
docker pull ghcr.io/<owner>/<repo>/bot:latest
docker pull ghcr.io/<owner>/<repo>/api:latest
docker pull ghcr.io/<owner>/<repo>/frontend:latest
```

Если команды выполняются успешно — образы публичны! ✅

## Проверка статуса образов

### Через веб-интерфейс

Перейдите на страницу образа в GitHub Packages. Под названием будет указано:
- 🔒 **Private** — образ приватный
- 🌐 **Public** — образ публичный

### Через docker pull (без авторизации)

```bash
# Выйти из ghcr.io (если были залогинены)
docker logout ghcr.io

# Попробовать скачать образ
docker pull ghcr.io/<owner>/<repo>/bot:latest
```

**Результат:**
- ✅ Образ скачивается — публичный доступ работает
- ❌ Ошибка "unauthorized" — образ все еще приватный

## Использование образов

### Локально

После того как образы стали публичными, их можно использовать локально:

```bash
cd devops

# Загрузить образы из registry
make pull

# Запустить сервисы из образов
make up-registry
```

Или напрямую через docker-compose:

```bash
docker compose -f docker-compose.registry.yml pull
docker compose -f docker-compose.registry.yml up
```

### На сервере (для спринта D2)

На удаленном сервере образы можно скачивать без авторизации:

```bash
# На сервере
docker pull ghcr.io/<owner>/<repo>/bot:latest
docker pull ghcr.io/<owner>/<repo>/api:latest
docker pull ghcr.io/<owner>/<repo>/frontend:latest

# Запустить через docker-compose
docker compose -f docker-compose.registry.yml up -d
```

## Приватные образы (опционально)

Если вы хотите оставить образы приватными, потребуется аутентификация.

### Создание Personal Access Token (PAT)

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Выбрать scope: `read:packages`
4. Скопировать токен

### Аутентификация

```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u <username> --password-stdin
```

Или через переменную окружения:

```bash
export CR_PAT=your_token_here
echo $CR_PAT | docker login ghcr.io -u <username> --password-stdin
```

После этого `docker pull` будет работать для приватных образов.

## Управление образами

### Просмотр тегов

На странице образа в GitHub Packages видны все доступные теги:
- `latest` — последняя версия
- `sha-abc1234` — конкретные коммиты

### Удаление старых версий

1. Перейти на страницу образа
2. Versions → выбрать версию
3. Delete this version

**Рекомендация:** Удаляйте старые версии по мере накопления для экономии места.

### Автоматическая очистка (будущее улучшение)

В будущем можно настроить GitHub Actions для автоматического удаления старых версий образов (retention policy).

## Troubleshooting

### Проблема: "unauthorized: unauthenticated"

**Причина:** Образ приватный, требуется аутентификация.

**Решение:**
1. Сделать образ публичным (см. выше)
2. Или аутентифицироваться через `docker login`

### Проблема: Образ не появляется в Packages

**Причина:** Workflow не выполнился или не был push event.

**Решение:**
1. Проверить GitHub Actions → Workflows → Build and Push Docker Images
2. Убедиться, что был push в ветку `day6-ci-draft`
3. Проверить логи workflow на наличие ошибок

### Проблема: "permission denied"

**Причина:** Недостаточно прав для публикации.

**Решение:**
1. Проверить `permissions` в workflow файле:
   ```yaml
   permissions:
     contents: read
     packages: write
   ```
2. Убедиться что GITHUB_TOKEN активен

### Проблема: Образ скачивается медленно

**Причина:** Большой размер образа или медленное соединение.

**Решение:**
- Оптимизировать Dockerfile (multi-stage builds) — планируется в будущих спринтах
- Использовать более быстрый интернет
- Кэшировать образы локально

## Дополнительная информация

### Лимиты GitHub Container Registry

Для публичных репозиториев:
- ✅ Неограниченное количество публичных образов
- ✅ Неограниченное количество скачиваний (pull)
- ✅ Бесплатное хранение публичных образов

Для приватных репозиториев:
- 500 MB хранилища (бесплатно)
- 1 GB трафика в месяц (бесплатно)
- За превышение — платно

### Официальная документация

- [Working with Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Publishing Docker images](https://docs.github.com/en/actions/publishing-packages/publishing-docker-images)

## Заключение

После настройки публичного доступа к образам:

✅ Образы можно скачивать без авторизации  
✅ Упрощается развертывание на серверах  
✅ Готовы к спринтам D2 (ручной deploy) и D3 (авто deploy)  

Не забудьте сделать все три образа (bot, api, frontend) публичными!

