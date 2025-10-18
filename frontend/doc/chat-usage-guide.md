# AI Chat Usage Guide

Quick reference for using the AI Chat feature implemented in Sprint F4.

---

## Accessing the Chat

1. Navigate to the dashboard at http://localhost:3000
2. Look for the floating blue/purple gradient button in the bottom-right corner
3. Click the button to open the chat panel

---

## Normal Mode

**Purpose:** General conversation with AI assistant

**How to use:**

1. Type your message in the input field
2. Press Enter or click the Send button
3. Wait for AI response (typing indicator shows)
4. Continue conversation naturally

**Example questions:**

- "Hello, how are you?"
- "Can you help me with Python programming?"
- "Tell me a joke"
- "Explain machine learning in simple terms"

---

## Admin Mode

**Purpose:** Analytics and statistics queries using natural language

**How to use:**

1. Toggle to "Admin" mode using the mode switcher
2. Ask analytics questions in natural language
3. AI will generate SQL query, execute it, and provide answer
4. SQL query is displayed below the answer for debugging

**Example analytics questions:**

1. **Basic counts:**
   - "How many messages are in the database?"
   - "How many users do we have?"
   - "Count total chats"

2. **Aggregations:**
   - "What is the average message length?"
   - "Show me message statistics"
   - "What's the total number of messages per role?"

3. **Time-based queries:**
   - "How many messages were sent today?"
   - "Show messages created in the last 7 days"
   - "What's the message count by date?"

4. **Grouping:**
   - "Show me top 10 users by message count"
   - "Which chat has the most messages?"
   - "Group messages by role and count them"

5. **Complex queries:**
   - "Show me the average message length per user"
   - "Find chats with more than 100 messages"
   - "What percentage of messages are from users vs assistants?"

---

## Features

### Message Display

- **User messages:** Appear on the right in light bubbles
- **AI messages:** Appear on the left in dark bubbles
- **Animations:** Smooth fade-in animations for all messages
- **Auto-scroll:** Chat automatically scrolls to latest message

### Mode Indicator

- **Blue badge:** Normal mode active
- **Purple badge:** Admin mode active
- Always visible in the chat header

### Typing Indicator

- Three animated dots appear when AI is thinking
- Helps you know the chat is processing your request

### SQL Query Display (Admin Mode Only)

- SQL query shown below the answer
- Useful for debugging and understanding how data was retrieved
- Can be used to learn SQL or verify query correctness

---

## Session Management

- **Session ID:** Automatically generated on first use
- **Storage:** Saved in browser localStorage
- **Persistence:** Maintained across page refreshes
- **Context:** All messages in a session share context
- **No expiration:** Session persists until localStorage is cleared

To start a fresh conversation:

1. Open browser developer tools (F12)
2. Go to Application → Local Storage
3. Delete the `chat_session_id` key
4. Refresh the page

---

## Safety Features (Admin Mode)

### Allowed:

- ✅ SELECT queries only
- ✅ Read-only operations
- ✅ JOINs, WHERE, GROUP BY, ORDER BY
- ✅ Aggregate functions (COUNT, AVG, SUM, etc.)

### Blocked:

- ❌ DROP (deleting tables)
- ❌ DELETE (removing records)
- ❌ UPDATE (modifying records)
- ❌ INSERT (adding records)
- ❌ ALTER (changing schema)
- ❌ CREATE (creating objects)
- ❌ TRUNCATE (clearing tables)
- ❌ GRANT/REVOKE (permissions)

All queries are validated before execution to ensure database safety.

---

## Troubleshooting

### Chat button doesn't appear

- Ensure frontend is running: `make frontend-dev`
- Check browser console for errors
- Verify you're on the dashboard page

### Messages don't send

- Ensure backend API is running: `make api-run`
- Check that API is accessible at http://localhost:8000
- Open Network tab in browser devtools to see API errors

### Admin mode returns errors

- Ensure database is running and accessible
- Check backend logs for SQL execution errors
- Verify your question can be translated to a SELECT query

### SQL query looks wrong (Admin mode)

- LLM might misunderstand the question - try rephrasing
- Be more specific about what you want
- Check the database schema in the query prompt

### Session context seems lost

- Check localStorage for `chat_session_id`
- Session might have been cleared
- Backend might have restarted (context stored in database)

---

## Technical Details

### Database Schema

```sql
-- Users table
users (
  id INTEGER PRIMARY KEY,
  created_at TIMESTAMP,
  is_deleted BOOLEAN
)

-- Messages table
messages (
  id INTEGER PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  chat_id INTEGER,
  role VARCHAR,  -- 'system', 'user', 'assistant'
  content TEXT,
  content_length INTEGER,
  created_at TIMESTAMP,
  is_deleted BOOLEAN
)
```

### API Endpoints

**Send Message:**

```http
POST /api/chat/message
Content-Type: application/json

{
  "session_id": "session_1729174800_abc123",
  "message": "Your message here",
  "mode": "normal" | "admin"
}
```

**Response:**

```json
{
  "message": "AI response",
  "sql_query": "SELECT ... (admin mode only)",
  "session_id": "session_1729174800_abc123"
}
```

---

## Best Practices

1. **Be specific in admin mode:** "Count messages from last 7 days" is better than "show me data"

2. **Use proper English:** LLM works best with clear, grammatically correct questions

3. **Start simple:** Test with basic questions before complex analytics

4. **Check SQL queries:** In admin mode, always review the generated SQL to understand what's being queried

5. **Clear context when needed:** If conversation context becomes confusing, clear localStorage and start fresh

---

## Known Limitations

1. No streaming responses (wait for full response)
2. No chat history retrieval API (messages stored but not easily retrievable)
3. No authentication (all users anonymous)
4. No file upload support
5. No message editing or deletion
6. Session never expires automatically

---

## Support

For issues or questions:

1. Check the backend logs: Look at terminal running `make api-run`
2. Check frontend console: Open browser devtools (F12)
3. Review `frontend/doc/sprint-f4-summary.md` for implementation details
4. Check API docs: http://localhost:8000/docs

---

**Enjoy chatting with your AI assistant!** 🤖✨
