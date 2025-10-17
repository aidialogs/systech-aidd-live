# 📖 Примеры использования

## Базовое использование

### Добавление чата на страницу

```tsx
import { FloatingChatButton } from '@/components/chat/floating-chat-button';

export default function MyPage() {
  return (
    <div>
      <h1>My Application</h1>
      {/* Ваш контент */}
      
      {/* Добавьте плавающую кнопку чата */}
      <FloatingChatButton />
    </div>
  );
}
```

## Примеры диалогов

### Normal Mode - Вопросы о программировании

**User:**
```
How do I sort an array in JavaScript?
```

**Assistant:**
```
You can sort an array in JavaScript using the sort() method:

const numbers = [3, 1, 4, 1, 5];
numbers.sort((a, b) => a - b); // [1, 1, 3, 4, 5]
```

### Admin SQL Mode - Запросы к базе данных

**User:**
```
Show me all users created in the last 7 days
```

**Assistant:**
```
Here are all users created in the last 7 days:

┌──────────────────┐
│ SQL Query        │
├──────────────────┤
│ SELECT *         │
│ FROM users       │
│ WHERE            │
│   created_at >=  │
│   NOW() -        │
│   INTERVAL       │
│   '7 days'       │
│ ORDER BY         │
│   created_at     │
│   DESC;          │
└──────────────────┘

Found 42 users.
```

**User:**
```
Count active subscriptions by plan
```

**Assistant:**
```
Here's the breakdown of active subscriptions:

┌────────────────────────────┐
│ SQL Query                  │
├────────────────────────────┤
│ SELECT                     │
│   plan_type,               │
│   COUNT(*) as count        │
│ FROM subscriptions         │
│ WHERE status = 'active'    │
│ GROUP BY plan_type         │
│ ORDER BY count DESC;       │
└────────────────────────────┘

- Premium: 150
- Basic: 320
- Free: 1200
```

## Кастомизация

### Использование отдельных компонентов

```tsx
import { ChatMessages, ChatInputForm, Message } from '@/components/chat/floating-chat-interface';

export function CustomChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  
  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 overflow-y-auto">
        <ChatMessages
          messages={messages}
          isLoading={false}
          error={null}
          mode="admin"
        />
      </div>
      
      <ChatInputForm
        input={input}
        setInput={setInput}
        onSubmit={(e) => {
          e.preventDefault();
          // Handle submit
        }}
        isLoading={false}
        mode="admin"
      />
    </div>
  );
}
```

### Кастомизация стилей

```tsx
import { ExpandableChat } from '@/components/ui/expandable-chat';

<ExpandableChat 
  size="lg"              // sm, md, lg
  position="bottom-left" // bottom-right, bottom-left
  icon={<MyCustomIcon />}
>
  {/* Ваш контент */}
</ExpandableChat>
```

## Интеграция с Backend

### Пример Backend API (FastAPI)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    mode: str
    user_id: int
    conversation_id: int

class ChatResponse(BaseModel):
    message: str
    sql_query: str | None = None

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if request.mode == "admin":
        # Генерация SQL запроса
        sql_query = generate_sql(request.message)
        result = execute_query(sql_query)
        
        return ChatResponse(
            message=format_results(result),
            sql_query=sql_query
        )
    else:
        # Обычный режим
        response = generate_response(request.message)
        return ChatResponse(message=response)

@app.get("/api/chat/history")
async def get_history(user_id: int, conversation_id: int):
    messages = fetch_history(user_id, conversation_id)
    return messages
```

## Тестирование

### Mock данные для тестирования

```tsx
const mockMessages: Message[] = [
  {
    id: 1,
    role: 'user',
    content: 'Show me all admin users',
  },
  {
    id: 2,
    role: 'assistant',
    content: 'Here are all admin users:',
    sql_query: 'SELECT * FROM users WHERE role = \'admin\' ORDER BY created_at DESC;',
  },
];
```

### Тестовый компонент

```tsx
import { ChatMessages } from '@/components/chat/floating-chat-interface';

export function ChatTest() {
  return (
    <ChatMessages
      messages={mockMessages}
      isLoading={false}
      error={null}
      mode="admin"
    />
  );
}
```

## Best Practices

### 1. Обработка ошибок

```tsx
try {
  const response = await sendChatMessage(message, mode, userId, conversationId);
  setMessages(prev => [...prev, response]);
} catch (error) {
  setError(error instanceof Error ? error.message : 'Unknown error');
  // Показать уведомление пользователю
}
```

### 2. Debouncing для автосохранения

```tsx
import { useEffect } from 'react';
import { debounce } from 'lodash';

const debouncedSave = debounce((messages) => {
  localStorage.setItem('chat-history', JSON.stringify(messages));
}, 1000);

useEffect(() => {
  debouncedSave(messages);
}, [messages]);
```

### 3. Оптимизация рендеринга

```tsx
import { memo } from 'react';

export const ChatMessage = memo(({ message }: { message: Message }) => {
  // Компонент не будет перерендериваться если message не изменился
  return <div>{message.content}</div>;
});
```

## Типичные сценарии

### Сценарий 1: Аналитика данных

```
User: "What's the average order value by month?"
