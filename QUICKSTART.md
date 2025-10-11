# 🚀 Быстрый старт для разработчиков

Этот проект использует **uv** для управления зависимостями и виртуальным окружением.

## Первоначальная настройка

### 1. Установка uv (если еще не установлен)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# или через pip
pip install uv
```

### 2. Установка зависимостей проекта

```bash
# Установить все зависимости (включая dev-инструменты)
make install

# или напрямую
uv sync --extra dev
```

Это автоматически создаст виртуальное окружение в `.venv/` и установит все зависимости из `pyproject.toml` и `uv.lock`.

### 3. Настройка переменных окружения

```bash
# Скопировать пример конфигурации
cp .env.example .env

# Отредактировать .env и заполнить:
# - BOT_TOKEN (от @BotFather в Telegram)
# - LLM_API_KEY (от OpenRouter или другого провайдера)
# - LLM_BASE_URL (URL API)
# - LLM_MODEL (название модели)
```

## Команды для разработки

### Основные команды

```bash
# Запуск бота
make run

# Запуск тестов
make test              # Все тесты
make test-cov          # Тесты без integration
make test-all          # Все тесты включая integration

# Проверка качества кода
make format            # Форматирование
make lint              # Линтинг и проверка типов
make check-all         # Полная проверка (format + lint + test-cov)

# Очистка
make clean             # Удалить логи и отчеты
```

### Использование uv напрямую

Все команды проекта должны запускаться через `uv run`:

```bash
# ✅ Правильно
uv run pytest tests/
uv run python -m src.main
uv run ruff check src/
uv run mypy src/

# ❌ Неправильно
python -m pytest
pytest tests/
```

### Почему uv run?

`uv run` автоматически:
- Активирует виртуальное окружение
- Использует правильные версии зависимостей из `uv.lock`
- Гарантирует воспроизводимость окружения

## Настройка VSCode

### Автоматическая настройка

Проект уже настроен для работы с VSCode:

1. Откройте проект в VSCode
2. Установите рекомендуемые расширения (VSCode предложит автоматически):
   - Python
   - Pylance
   - Ruff
   - Python Debugger

3. VSCode автоматически использует `.venv/bin/python` как интерпретатор

### Доступные конфигурации запуска (F5)

- **Python: Run Bot** - запуск бота с отладкой
- **Python: Run All Tests** - запуск всех тестов
- **Python: Run Tests (No Integration)** - только unit-тесты
- **Python: Run Tests with Coverage** - тесты с измерением покрытия
- **Python: Debug Current Test File** - отладка текущего файла тестов

### Доступные задачи (Cmd+Shift+P → Tasks: Run Task)

- Install Dependencies
- Run Bot
- Run Tests
- Format Code
- Lint Code
- Check All
- Clean Build Artifacts

## Workflow разработки

### 1. Перед началом работы

```bash
# Убедитесь, что зависимости актуальны
uv sync --extra dev
```

### 2. Во время разработки

```bash
# Написали код → Форматирование
make format

# Проверка качества
make lint

# Запуск тестов
make test
```

### 3. Перед коммитом

```bash
# Полная проверка
make check-all
```

Все должно быть зеленым:
- ✅ Ruff: 0 warnings
- ✅ Mypy: 0 errors
- ✅ Tests: 30/30 passed
- ✅ Coverage: 100%

## Структура проекта

```
systech-aidd-live/
├── .venv/              # Виртуальное окружение (создается автоматически)
├── .vscode/            # Настройки VSCode
├── src/                # Исходный код
├── tests/              # Тесты
├── doc/                # Документация
├── logs/               # Логи
├── pyproject.toml      # Зависимости и настройки инструментов
├── uv.lock             # Lock-файл зависимостей (для воспроизводимости)
├── Makefile            # Команды автоматизации
└── README.md           # Полная документация
```

## Решение проблем

### "Command not found: uv"

```bash
# Установите uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Перезапустите терминал
```

### "No module named XXX"

```bash
# Переустановите зависимости
uv sync --extra dev
```

### "Tests fail in VSCode but pass in terminal"

VSCode должен использовать правильный интерпретатор:
1. Cmd+Shift+P → "Python: Select Interpreter"
2. Выберите `.venv/bin/python`

### "pytest: error: unrecognized arguments: --cov"

```bash
# Установите dev-зависимости
uv sync --extra dev
```

## Дополнительная информация

- 📚 **Полная документация**: см. `README.md`
- 🏗️ **Архитектурные решения**: см. `doc/adrs/`
- 📝 **План разработки**: см. `doc/tasklist.md`
- 💡 **Видение проекта**: см. `doc/vision.md`

## Полезные ссылки

- [uv Documentation](https://docs.astral.sh/uv/)
- [aiogram Documentation](https://docs.aiogram.dev/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)

---

**Готово к работе!** 🎉

Теперь вы можете начать разработку с правильно настроенным окружением.

