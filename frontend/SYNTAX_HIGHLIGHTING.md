# SQL Syntax Highlighting в Admin режиме

## Описание

В админ режиме Devil AI Assistant отображает SQL запросы с красивой подсветкой синтаксиса, используя библиотеку `react-syntax-highlighter`.

## Как это работает

### 1. Компонент ChatMessages

В файле `src/components/chat/floating-chat-interface.tsx` реализована логика отображения SQL с подсветкой:

```tsx
{mode === 'admin' && message.role === 'assistant' && message.sql_query && (
  <div className="mt-3 rounded-md overflow-hidden border border-border">
    <div className="bg-muted/50 px-3 py-1 text-xs font-semibold text-muted-foreground border-b border-border">
      SQL Query
    </div>
    <SyntaxHighlighter
      language="sql"
      style={vscDarkPlus}
      customStyle={{
        margin: 0,
        padding: '0.75rem',
        fontSize: '0.875rem',
        borderRadius: 0,
      }}
      showLineNumbers={false}
    >
      {message.sql_query}
    </SyntaxHighlighter>
  </div>
)}
```

### 2. Условия отображения

SQL запрос отображается только когда:
- ✅ `mode === 'admin'` - включен админ режим
- ✅ `message.role === 'assistant'` - сообщение от ассистента
- ✅ `message.sql_query` - присутствует SQL запрос в ответе

### 3. Стилизация

- **Тема**: `vscDarkPlus` - темная тема в стиле Visual Studio Code
- **Заголовок**: "SQL Query" с серым фоном
- **Граница**: тонкая граница для отделения от основного текста
- **Шрифт**: моноширинный, размер 0.875rem
- **Отступы**: 0.75rem внутренние отступы

## Пример использования

### Backend ответ

Backend должен возвращать ответ в формате:

```json
{
  "message": "Вот список всех администраторов:",
  "sql_query": "SELECT * FROM users WHERE role = 'admin' ORDER BY created_at DESC LIMIT 10;"
}
```

### Отображение в UI

```
┌─────────────────────────────────────────────┐
│ Вот список всех администраторов:            │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ SQL Query                               │ │
│ ├─────────────────────────────────────────┤ │
│ │ SELECT * FROM users                     │ │
│ │ WHERE role = 'admin'                    │ │
│ │ ORDER BY created_at DESC                │ │
│ │ LIMIT 10;                               │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

## Поддерживаемые SQL ключевые слова

Подсветка синтаксиса работает для всех стандартных SQL ключевых слов:

- **DDL**: `CREATE`, `ALTER`, `DROP`, `TRUNCATE`
- **DML**: `SELECT`, `INSERT`, `UPDATE`, `DELETE`
- **Clauses**: `FROM`, `WHERE`, `JOIN`, `GROUP BY`, `ORDER BY`, `HAVING`
- **Functions**: `COUNT`, `SUM`, `AVG`, `MAX`, `MIN`
- **Operators**: `AND`, `OR`, `NOT`, `IN`, `LIKE`, `BETWEEN`
- **Types**: `VARCHAR`, `INT`, `DATE`, `TIMESTAMP`, etc.
- **Strings**: подсветка строковых литералов
- **Numbers**: подсветка числовых значений
- **Comments**: `--` и `/* */`

## Настройка темы

Если нужно изменить тему подсветки, в файле `floating-chat-interface.tsx` измените импорт:

```tsx
// Текущая тема
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

// Другие доступные темы:
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { dracula } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { nord } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
```

## Производительность

- Используется динамический импорт для оптимизации bundle size
- Подсветка применяется только в админ режиме
- Рендеринг происходит только при наличии SQL запроса

## Зависимости

```json
{
  "react-syntax-highlighter": "^15.5.0",
  "@types/react-syntax-highlighter": "^15.5.13"
}
```

