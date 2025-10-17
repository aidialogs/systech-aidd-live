# 🚀 Quick Start Guide

## Установка зависимостей

```bash
cd frontend
npm install
```

## Запуск в режиме разработки

```bash
npm run dev
```

Приложение будет доступно по адресу: http://localhost:3000

## Основные возможности

### ✨ Подсветка SQL синтаксиса

В **Admin SQL режиме** все SQL запросы отображаются с красивой подсветкой синтаксиса:

- 🎨 Цветная подсветка ключевых слов SQL
- 📝 Моноширинный шрифт для лучшей читаемости
- 🌙 Темная тема VS Code (vscDarkPlus)
- 📋 Отдельный блок для SQL с заголовком

### 🔄 Переключение режимов

- **Normal Mode** 💻 - обычный AI ассистент для вопросов о программировании
- **Admin SQL Mode** 🗄️ - запросы к базе данных на естественном языке

### 💬 Интерфейс чата

- Плавающая кнопка в правом нижнем углу
- Раскрывающееся окно чата
- История сообщений
- Автоматическая прокрутка к последнему сообщению
- Поддержка Enter для отправки (Shift+Enter для новой строки)

## Архитектура компонентов

```
FloatingChatButton (главный компонент)
├── ExpandableChat (контейнер)
│   ├── ExpandableChatHeader
│   │   ├── Заголовок
│   │   └── ModeToggle (переключатель режимов)
│   ├── ExpandableChatBody
│   │   └── ChatMessages (отображение сообщений)
│   │       └── SQL Syntax Highlighter (для админ режима)
│   └── ExpandableChatFooter
│       └── ChatInputForm (форма ввода)
```

## API Endpoints

### POST /api/chat
Отправка сообщения в чат

**Request:**
```json
{
  "message": "Show me all admin users",
  "mode": "admin",
  "user_id": 1,
  "conversation_id": 1
}
```

**Response:**
```json
{
  "message": "Here are all admin users:",
  "sql_query": "SELECT * FROM users WHERE role = 'admin' ORDER BY created_at DESC;"
}
```

### GET /api/chat/history
Получение истории чата

**Query Parameters:**
- `user_id` - ID пользователя
- `conversation_id` - ID конверсации

**Response:**
```json
[
  {
    "role": "user",
    "content": "Show me all admin users"
  },
  {
    "role": "assistant",
    "content": "Here are all admin users:",
    "sql_query": "SELECT * FROM users WHERE role = 'admin';"
  }
]
```

## Настройка Backend Proxy

В `next.config.js` настроен прокси для API запросов:

```javascript
async rewrites() {
  return [
    {
      source: '/api/:path*',
      destination: 'http://localhost:8000/api/:path*',
    },
  ];
}
```

Убедитесь, что ваш backend запущен на порту 8000.

## Кастомизация

### Изменение темы SQL подсветки

В `src/components/chat/floating-chat-interface.tsx`:

```tsx
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
// Измените на другую тему, например:
// import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
```

### Изменение цветовой схемы

В `src/app/globals.css` настройте CSS переменные:

```css
:root {
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
  /* ... другие переменные */
}
```

## Troubleshooting

### Ошибка при подключении к API

Проверьте, что:
1. Backend запущен на порту 8000
2. Proxy настроен в `next.config.js`
3. CORS настроен на backend

### Подсветка SQL не работает

Убедитесь, что:
1. Установлен пакет `react-syntax-highlighter`
2. Backend возвращает поле `sql_query` в ответе
3. Включен Admin режим

## Build для продакшена

```bash
npm run build
npm start
```

## Лицензия

MIT
