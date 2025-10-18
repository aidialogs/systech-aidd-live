# ADR-06: Выбор PostgreSQL + SQLAlchemy 2.0 + Alembic для персистентного хранения

**Дата:** 2025-01-16  
**Статус:** Принято  
**Авторы:** systech-aidd team  
**Связанные ADR:** ADR-02 (async-first architecture)

## Контекст

В Sprint S0 мы использовали in-memory хранилище для контекста диалогов. Это простое решение, но имеет критические недостатки:

- **Потеря данных при перезапуске** - вся история диалогов теряется
- **Нет масштабируемости** - невозможно распределить нагрузку на несколько инстансов бота
- **Нет аналитики** - невозможно анализировать историю взаимодействий пользователей
- **Ограниченные возможности** - нет архивирования, нет восстановления, нет поиска по истории

В Sprint S1 необходимо перейти к персистентному хранилищу данных.

## Требования

1. **Персистентность** - данные должны сохраняться между перезапусками
2. **KISS** - простое решение, минимум оверинжиниринга
3. **Async support** - совместимость с aiogram (async framework)
4. **Type safety** - строгая типизация с mypy strict mode
5. **Developer experience** - удобство разработки и генерации кода с помощью LLM
6. **Миграции** - управление схемой БД с version control
7. **Soft delete** - логическое удаление данных для возможной аналитики
8. **Production ready** - готовность к продакшену

## Рассмотренные альтернативы

### 1. SQLite + SQLAlchemy 2.0 + Alembic

**Плюсы:**
- ✅ Максимальная простота (файловая БД, нет сервера)
- ✅ Отличная подходит для KISS принципа
- ✅ Быстрый старт разработки

**Минусы:**
- ❌ Ограничения при масштабировании (file-based locking)
- ❌ Проблемы с batch операциями в Alembic (requires `render_as_batch=True`)
- ❌ Ограниченная конкурентность при записи

**Вердикт:** Хороший выбор для MVP, но не подходит для роста проекта.

### 2. PostgreSQL + Raw SQL + Yoyo Migrations

**Плюсы:**
- ✅ Производительность и надежность PostgreSQL
- ✅ Полный контроль над SQL запросами
- ✅ Простые SQL-based миграции

**Минусы:**
- ❌ Много boilerplate кода
- ❌ Отсутствие type safety
- ❌ Сложнее генерировать и поддерживать с LLM
- ❌ Больше ошибок при ручном написании SQL

**Вердикт:** Слишком низкий уровень абстракции для наших задач.

### 3. Tortoise ORM + Aerich

**Плюсы:**
- ✅ Django-style ORM (знакомый синтаксис)
- ✅ Native async support
- ✅ Простой в использовании

**Минусы:**
- ❌ Меньшее комьюнити по сравнению с SQLAlchemy
- ❌ Менее зрелая экосистема
- ❌ Ограниченная функциональность для сложных запросов

**Вердикт:** Хорошая альтернатива, но SQLAlchemy более production-ready.

### 4. Peewee ORM

**Плюсы:**
- ✅ Простой и минималистичный
- ✅ Легкий в изучении

**Минусы:**
- ❌ Нет native async support (требует `peewee-async`)
- ❌ Менее подходит для async-first архитектуры
- ❌ Меньшая экосистема

**Вердикт:** Не подходит из-за отсутствия полноценной async поддержки.

## Решение: PostgreSQL + SQLAlchemy 2.0 + Alembic + asyncpg

### Выбранный стек

- **БД:** PostgreSQL 16 (в Docker контейнере для разработки)
- **ORM:** SQLAlchemy 2.0 с async поддержкой
- **Driver:** asyncpg (высокопроизводительный async драйвер)
- **Migrations:** Alembic с autogenerate из моделей

### Обоснование

**PostgreSQL:**
- ✅ Production-ready СУБД с доказанной надежностью
- ✅ Отличная производительность для нашей нагрузки
- ✅ Масштабируемость (vertical + horizontal через replicas)
- ✅ Богатая экосистема инструментов
- ✅ Docker - простой деплой для dev и prod окружений

**SQLAlchemy 2.0:**
- ✅ De-facto стандарт ORM для Python
- ✅ Полноценная async поддержка (native, не через пул потоков)
- ✅ Строгая типизация с `Mapped[]` и type hints
- ✅ Отличная совместимость с mypy
- ✅ LLM-friendly - Claude и другие LLM хорошо знают SQLAlchemy
- ✅ Декларативный стиль моделей - легко читать и генерировать код
- ✅ Зрелая экосистема, огромное комьюнити

**asyncpg:**
- ✅ Fastest async PostgreSQL driver для Python
- ✅ Native async (не blocking)
- ✅ Идеальное сочетание с aiogram (оба async)

**Alembic:**
- ✅ Автогенерация миграций из SQLAlchemy моделей
- ✅ Version control для схемы БД (git-friendly)
- ✅ Безопасные миграции (up/down)
- ✅ Интеграция с SQLAlchemy из коробки

### Архитектурные решения

**1. Repository Pattern**
- Инкапсуляция логики работы с БД
- Легкость тестирования (mock repository)
- Чистая архитектура

**2. Session Management**
- `async_sessionmaker` - фабрика сессий
- ContextManager создает сессию для каждой операции
- Автоматический rollback при ошибках

**3. Soft Delete Strategy**
- Поле `is_deleted` вместо физического удаления
- Возможность аналитики и восстановления данных
- Фильтрация `WHERE is_deleted = False` во всех запросах

**4. Context Limiting**
- Ограничение при чтении (LIMIT в SQL)
- Полная история сохранена в БД
- System prompt всегда включается первым

## Последствия

### Положительные

✅ **Персистентность** - данные сохраняются между перезапусками  
✅ **Масштабируемость** - готовность к росту проекта  
✅ **Type Safety** - строгая типизация с mypy  
✅ **Developer Experience** - удобство разработки и генерации кода  
✅ **Production Ready** - надежное решение для продакшена  
✅ **Аналитика** - возможность анализа истории взаимодействий  

### Риски и недостатки

⚠️ **Усложнение деплоя** - требуется PostgreSQL сервер (решается через Docker)  
⚠️ **Зависимость от БД** - необходимость мониторинга и бэкапов  
⚠️ **Оверхед async** - незначительное усложнение кода (async/await)  

### Требования к окружению

**Development:**
- Docker Compose для локального PostgreSQL
- Environment variable `DATABASE_URL`

**Production:**
- PostgreSQL 16+ (cloud provider или self-hosted)
- Connection pooling (pg_bouncer recommended)
- Regular backups

## Миграция с S0

Переход с in-memory на PostgreSQL:

1. ✅ Создание SQLAlchemy моделей
2. ✅ Настройка Alembic миграций
3. ✅ Рефакторинг ContextManager под async repository
4. ✅ Интеграция DB lifecycle в main.py
5. ✅ Обновление тестов под async

**Backward compatibility:** Нет - breaking change, требуется очистка старого контекста.

## Ссылки

- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/)
- [asyncpg Documentation](https://magicstack.github.io/asyncpg/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Обновления

- **2025-01-16**: Первая версия

