# ADR-03: Инструменты качества кода

**Статус:** Принято  
**Дата:** 2025-10-11  
**Контекст:** Устранение технического долга, Итерация 0

---

## Контекст

После завершения MVP возникла необходимость повысить качество кода:
- Отсутствие автоматических проверок
- Нет type hints и статического анализа
- Низкое покрытие тестами (~30%)
- Нет единого стиля кода
- Ручная проверка качества

## Решение

Интегрировать современные инструменты качества:

**1. Ruff** - универсальный инструмент для:
- Форматирования кода (замена black)
- Линтинга (замена flake8, pylint, isort)
- Проверки соглашений об именовании
- Проверки type hints

**2. Mypy** - статическая проверка типов:
- Strict mode для максимальной строгости
- Проверка всех функций и методов
- Ранее выявление ошибок

**3. Pytest-cov** - измерение покрытия:
- Интеграция с pytest
- HTML и terminal отчеты
- Цель: ≥90% coverage

**4. Pytest-mock** - моки для тестов:
- Изоляция от внешних зависимостей
- AsyncMock для асинхронного кода
- Упрощение написания тестов

**5. Makefile** - автоматизация команд:
- `make format` - форматирование
- `make lint` - проверка качества
- `make test-cov` - тесты с coverage
- `make check-all` - полная проверка

## Конфигурация

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "ANN", "B", "A", "C4", "DTZ", 
          "PIE", "PT", "RET", "SIM", "ARG", "ERA", "RUF"]

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
addopts = "--cov=src --cov-report=term-missing --cov-report=html"
```

## Альтернативы

**Вариант 1: Black + Flake8 + Pylint**
- ❌ Медленнее (3 инструмента вместо 1)
- ❌ Больше конфигурации
- ❌ Возможны конфликты правил

**Вариант 2: Только mypy**
- ❌ Нет проверки стиля кода
- ❌ Нет автоформатирования

**Вариант 3: Pre-commit hooks**
- ❌ Замедляют коммиты
- ❌ Усложняют workflow
- ✅ Выбрали ручной запуск через `make`

## Последствия

**Положительные:**
- ✅ Единый инструмент (ruff) для форматирования и линтинга
- ✅ Быстрая проверка (ruff написан на Rust)
- ✅ Строгая типизация (mypy strict mode)
- ✅ Автоматизация через Makefile
- ✅ Явный контроль (ручной запуск, не pre-commit)

**Отрицательные:**
- ⚠️ Требуется время на исправление baseline ошибок
- ⚠️ Необходимость добавлять type hints во весь код

**Метрики после внедрения:**
- Ruff warnings: 64 → 0
- Mypy errors: 64 → 0  
- Test coverage: 30% → 100%
- Time to run checks: ~3s

## Примечания

- Инструменты запускаются **вручную**, не через pre-commit
- Команды документированы в README.md
- Добавлены в `.cursor/rules/conventions.mdc` и `workflow.mdc`
- Конфигурация в `pyproject.toml` (единый файл)

## Ссылки

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Mypy Strict Mode](https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-strict)
- [Pytest Coverage Plugin](https://pytest-cov.readthedocs.io/)

