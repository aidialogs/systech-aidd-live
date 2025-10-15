# 🎨 Visual Overview - Визуальный обзор проекта

**Цель**: Понять проект через визуализации  
**Для кого**: Визуальное мышление, быстрое понимание архитектуры  
**Время**: 30-40 минут

> 💡 Этот гайд содержит только диаграммы с минимальными комментариями.  
> Для детальных объяснений см. другие гайды.

---

## 📊 Содержание визуализаций

1. [Системная архитектура](#-1-системная-архитектура)
2. [Структура классов](#-2-структура-классов)
3. [Потоки данных](#-3-потоки-данных)
4. [Сценарии взаимодействия](#-4-сценарии-взаимодействия)
5. [Жизненные циклы](#-5-жизненные-циклы)
6. [Структура проекта](#-6-структура-проекта)
7. [User Journey](#-7-user-journey)
8. [Процессы разработки](#-8-процессы-разработки)
9. [Error Handling](#-9-error-handling)
10. [История проекта](#-10-история-проекта)

---

## 🏗️ 1. Системная архитектура

### 1.1 High-Level System Architecture

```mermaid
graph TB
    subgraph External["🌐 External Systems"]
        User[👤 User<br/>Telegram Client]
        TelegramAPI[📱 Telegram Bot API<br/>telegram.org]
        OpenRouter[🧠 OpenRouter API<br/>LLM Provider]
    end
    
    subgraph Application["🤖 Bot Application"]
        subgraph Core["Core Layer"]
            Main[main.py<br/>Entry Point]
            Config[Config<br/>Configuration]
        end
        
        subgraph Handlers["Handler Layer"]
            MsgHandler[MessageHandler<br/>Coordinator]
            CmdHandler[CommandHandler<br/>Commands]
        end
        
        subgraph Services["Service Layer"]
            LLMClient[LLMClient<br/>AI Integration]
            CtxManager[ContextManager<br/>State Management]
        end
        
        subgraph Models["Model Layer"]
            Message[Message<br/>Data Model]
            Protocols[Protocols<br/>Interfaces]
        end
    end
    
    subgraph Storage["💾 Storage"]
        Memory[(In-Memory<br/>Context Dict)]
        Logs[(Logs<br/>app.log)]
        Prompts[(Prompts<br/>system_prompt.txt)]
    end
    
    User <-->|messages| TelegramAPI
    TelegramAPI <-->|aiogram| Main
    Main --> Config
    Main --> MsgHandler
    
    MsgHandler --> CmdHandler
    MsgHandler --> LLMClient
    MsgHandler --> CtxManager
    
    CmdHandler --> CtxManager
    
    LLMClient <-->|API calls| OpenRouter
    CtxManager --> Memory
    
    Config --> Prompts
    MsgHandler --> Logs
    
    Message -.->|uses| MsgHandler
    Message -.->|uses| CtxManager
    Protocols -.->|defines| LLMClient
    Protocols -.->|defines| CtxManager
    
    style User fill:#3498DB,stroke:#ECF0F1,stroke-width:3px,color:#ECF0F1
    style TelegramAPI fill:#34495E,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style OpenRouter fill:#9B59B6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Main fill:#E74C3C,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style MsgHandler fill:#E74C3C,stroke:#ECF0F1,stroke-width:3px,color:#ECF0F1
    style CmdHandler fill:#27AE60,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style LLMClient fill:#9B59B6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style CtxManager fill:#F39C12,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Memory fill:#95A5A6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style External fill:#2C3E50,stroke:#ECF0F1,color:#ECF0F1
    style Application fill:#34495E,stroke:#ECF0F1,color:#ECF0F1
    style Storage fill:#2C3E50,stroke:#ECF0F1,color:#ECF0F1
```

### 1.2 Deployment View

```mermaid
graph LR
    subgraph Developer["💻 Developer Machine"]
        Code[Source Code<br/>src/]
        Tests[Tests<br/>tests/]
        Env[Environment<br/>.venv/]
    end
    
    subgraph Runtime["🚀 Runtime"]
        Process[Python Process<br/>main.py]
        Polling[Polling Loop<br/>aiogram]
    end
    
    subgraph External["🌐 External Services"]
        Telegram[Telegram<br/>Bot API]
        LLM[OpenRouter<br/>LLM API]
    end
    
    Code --> Process
    Tests -.->|validation| Process
    Env --> Process
    
    Process --> Polling
    Polling <-->|long polling| Telegram
    Process <-->|HTTP/REST| LLM
    
    style Developer fill:#2C3E50,stroke:#ECF0F1,color:#ECF0F1
    style Runtime fill:#34495E,stroke:#ECF0F1,color:#ECF0F1
    style External fill:#2C3E50,stroke:#ECF0F1,color:#ECF0F1
    style Process fill:#E74C3C,stroke:#ECF0F1,stroke-width:3px,color:#ECF0F1
    style Telegram fill:#3498DB,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style LLM fill:#9B59B6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
```

---

## 🧩 2. Структура классов

### 2.1 Class Diagram

```mermaid
classDiagram
    class Message {
        +str role
        +str content
        +__init__(role, content)
        +to_dict() dict
    }
    
    class Config {
        +str bot_token
        +str llm_api_key
        +str llm_base_url
        +str llm_model
        +str system_prompt
        +int max_context_messages
        +from_env() Config
    }
    
    class LLMClientProtocol {
        <<interface>>
        +get_response(messages) str
    }
    
    class ContextManagerProtocol {
        <<interface>>
        +add_message(user_id, chat_id, message)
        +get_context(user_id, chat_id) list
        +clear_context(user_id, chat_id)
    }
    
    class LLMClient {
        -AsyncOpenAI client
        -str model
        +__init__(api_key, base_url, model)
        +get_response(messages) str
    }
    
    class ContextManager {
        -dict contexts
        -int max_context_messages
        +__init__(max_context_messages)
        +add_message(user_id, chat_id, message)
        +get_context(user_id, chat_id) list
        +clear_context(user_id, chat_id)
        -_get_key(user_id, chat_id) tuple
        -_create_context(key)
        -_trim_context(key)
    }
    
    class CommandHandler {
        -ContextManagerProtocol context_manager
        -str system_prompt
        +__init__(context_manager, system_prompt)
        +handle_command(text, user_id, chat_id) str|None
        -_handle_start() str
        -_handle_help() str
        -_handle_reset(user_id, chat_id) str
        -_handle_role() str
        -_get_help_text() str
    }
    
    class MessageHandler {
        -LLMClientProtocol llm_client
        -ContextManagerProtocol context_manager
        -CommandHandler command_handler
        -str system_prompt
        +__init__(llm_client, context_manager, command_handler, system_prompt)
        +handle_message(message, user_id, chat_id) str
    }
    
    LLMClient ..|> LLMClientProtocol
    ContextManager ..|> ContextManagerProtocol
    
    MessageHandler --> LLMClientProtocol
    MessageHandler --> ContextManagerProtocol
    MessageHandler --> CommandHandler
    
    CommandHandler --> ContextManagerProtocol
    
    ContextManager --> Message
    LLMClient --> Message
    MessageHandler --> Message
    
    style Message fill:#3498DB,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Config fill:#27AE60,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style LLMClientProtocol fill:#95A5A6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style ContextManagerProtocol fill:#95A5A6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style LLMClient fill:#9B59B6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style ContextManager fill:#F39C12,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style CommandHandler fill:#27AE60,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style MessageHandler fill:#E74C3C,stroke:#ECF0F1,stroke-width:3px,color:#ECF0F1
```

### 2.2 Dependency Graph

```mermaid
graph TD
    main[main.py] --> config[config.py]
    main --> msg_handler[message_handler.py]
    main --> cmd_handler[command_handler.py]
    main --> llm[llm_client.py]
    main --> ctx[context_manager.py]
    
    msg_handler --> protocols[protocols.py]
    msg_handler --> message[message.py]
    msg_handler --> exceptions[exceptions.py]
    
    cmd_handler --> protocols
    
    llm --> protocols
    llm --> message
    llm --> exceptions
    
    ctx --> protocols
    ctx --> message
    
    config --> exceptions
    
    style main fill:#E74C3C,stroke:#ECF0F1,stroke-width:3px,color:#ECF0F1
    style msg_handler fill:#E74C3C,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style cmd_handler fill:#27AE60,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style llm fill:#9B59B6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style ctx fill:#F39C12,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style protocols fill:#95A5A6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style message fill:#3498DB,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style exceptions fill:#E67E22,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style config fill:#27AE60,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
```

---

## 🔄 3. Потоки данных

### 3.1 Complete Data Flow

```mermaid
graph LR
    A[User Input<br/>Telegram] --> B[Bot<br/>Dispatcher]
    B --> C{Message Type?}
    
    C -->|Command| D[CommandHandler]
    C -->|Text| E[MessageHandler]
    
    D --> F[ContextManager]
    
    E --> G[Get Context]
    G --> F
    F --> H[Context<br/>History]
    H --> E
    
    E --> I[Add User<br/>Message]
    I --> F
    
    E --> J[LLMClient]
    J --> K[OpenRouter<br/>API]
    K --> L[AI Response]
    L --> J
    J --> E
    
    E --> M[Add Assistant<br/>Message]
    M --> F
    
    E --> N[Response]
    D --> N
    N --> B
    B --> O[User Output<br/>Telegram]
    
    style A fill:#3498DB,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style B fill:#2C3E50,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style D fill:#27AE60,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style E fill:#E74C3C,stroke:#ECF0F1,stroke-width:3px,color:#ECF0F1
    style F fill:#F39C12,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style J fill:#9B59B6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style K fill:#34495E,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style O fill:#3498DB,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
```

### 3.2 Context Data Flow

```mermaid
graph TB
    subgraph Input["📥 Input"]
        U1[User Message<br/>'Привет']
    end
    
    subgraph ContextManager["💾 ContextManager"]
        Check{Context<br/>exists?}
        Create[Create Context<br/>+ system prompt]
        Get[Get Context]
        Add[Add Message]
        Trim{Size ><br/>max?}
        TrimAction[Trim to max<br/>keep system]
    end
    
    subgraph Storage["🗄️ Storage"]
        Dict["contexts = {<br/>(user_id, chat_id):<br/>[Messages]<br/>}"]
    end
    
    subgraph Output["📤 Output"]
        Context[Context<br/>list[Message]]
    end
    
    U1 --> Check
    Check -->|No| Create
    Check -->|Yes| Get
    Create --> Dict
    Get --> Dict
    Dict --> Add
    Add --> Trim
    Trim -->|Yes| TrimAction
    Trim -->|No| Context
    TrimAction --> Dict
    Dict --> Context
    
    style U1 fill:#3498DB,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Dict fill:#95A5A6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Context fill:#27AE60,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Check fill:#F39C12,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Trim fill:#E67E22,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style ContextManager fill:#2C3E50,stroke:#ECF0F1,color:#ECF0F1
    style Input fill:#34495E,stroke:#ECF0F1,color:#ECF0F1
    style Storage fill:#34495E,stroke:#ECF0F1,color:#ECF0F1
    style Output fill:#34495E,stroke:#ECF0F1,color:#ECF0F1
```

---

## 🎬 4. Сценарии взаимодействия

### 4.1 Regular Message Flow

```mermaid
sequenceDiagram
    autonumber
    participant U as 👤 User
    participant T as Telegram API
    participant B as Bot
    participant MH as MessageHandler
    participant CM as ContextManager
    participant LC as LLMClient
    participant API as OpenRouter

    U->>T: Send "Привет"
    T->>B: Webhook/Polling
    B->>MH: handle_message(msg, user_id, chat_id)
    
    rect rgb(52, 73, 94)
        Note over MH,CM: Context Management
        MH->>CM: get_context(user_id, chat_id)
        CM-->>MH: [system, prev messages...]
        MH->>CM: add_message(user, "Привет")
        CM-->>MH: ✓
    end
    
    rect rgb(155, 89, 182)
        Note over MH,API: LLM Processing
        MH->>LC: get_response(messages)
        LC->>API: POST /chat/completions
        API-->>LC: {"choices": [...]}
        LC-->>MH: "Здравствуйте!"
    end
    
    rect rgb(52, 73, 94)
        Note over MH,CM: Save Response
        MH->>CM: add_message(assistant, "Здравствуйте!")
        CM-->>MH: ✓
    end
    
    MH-->>B: "Здравствуйте!"
    B->>T: Send message
    T->>U: "Здравствуйте!"
    
    style U fill:#3498DB,stroke:#ECF0F1,color:#ECF0F1
    style T fill:#34495E,stroke:#ECF0F1,color:#ECF0F1
    style B fill:#2C3E50,stroke:#ECF0F1,color:#ECF0F1
    style MH fill:#E74C3C,stroke:#ECF0F1,color:#ECF0F1
    style CM fill:#F39C12,stroke:#ECF0F1,color:#ECF0F1
    style LC fill:#9B59B6,stroke:#ECF0F1,color:#ECF0F1
    style API fill:#34495E,stroke:#ECF0F1,color:#ECF0F1
```

### 4.2 Command Flow (/reset)

```mermaid
sequenceDiagram
    autonumber
    participant U as 👤 User
    participant T as Telegram
    participant B as Bot
    participant MH as MessageHandler
    participant CH as CommandHandler
    participant CM as ContextManager

    U->>T: Send "/reset"
    T->>B: Message
    B->>MH: handle_message("/reset", ...)
    
    MH->>MH: Check if command
    Note over MH: text.startswith("/")
    
    MH->>CH: handle_command("/reset", user_id, chat_id)
    
    CH->>CM: clear_context(user_id, chat_id)
    CM->>CM: del contexts[key]
    CM-->>CH: ✓
    
    CH-->>MH: "История диалога очищена"
    MH-->>B: "История диалога очищена"
    B->>T: Send
    T->>U: "История диалога очищена"
    
    style U fill:#3498DB,stroke:#ECF0F1,color:#ECF0F1
    style MH fill:#E74C3C,stroke:#ECF0F1,color:#ECF0F1
    style CH fill:#27AE60,stroke:#ECF0F1,color:#ECF0F1
    style CM fill:#F39C12,stroke:#ECF0F1,color:#ECF0F1
```

### 4.3 Error Handling Flow

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant MH as MessageHandler
    participant LC as LLMClient
    participant API as OpenRouter

    U->>MH: Send message
    MH->>LC: get_response(messages)
    LC->>API: POST /chat/completions
    
    alt Success
        API-->>LC: Response
        LC-->>MH: AI response
        MH-->>U: AI response
    else API Error
        API--xLC: Timeout/Error
        LC->>LC: raise LLMError
        LC--xMH: LLMError
        MH->>MH: Log error
        MH-->>U: "Извините, временные проблемы..."
    else General Error
        LC--xMH: Exception
        MH->>MH: Log exception
        MH-->>U: "Произошла ошибка..."
    end
    
    style U fill:#3498DB,stroke:#ECF0F1,color:#ECF0F1
    style MH fill:#E74C3C,stroke:#ECF0F1,color:#ECF0F1
    style LC fill:#9B59B6,stroke:#ECF0F1,color:#ECF0F1
    style API fill:#34495E,stroke:#ECF0F1,color:#ECF0F1
```

---

## 🔄 5. Жизненные циклы

### 5.1 Context Lifecycle

```mermaid
stateDiagram-v2
    [*] --> NonExistent: Start
    
    NonExistent --> Created: First message<br/>from user
    
    Created --> Active: Add message
    
    state Active {
        [*] --> Normal
        Normal --> Normal: Add user message
        Normal --> Normal: Add assistant message
        Normal --> CheckSize: After add
        CheckSize --> Normal: size <= max
        CheckSize --> Trimming: size > max
        Trimming --> Normal: Trim old messages<br/>(keep system)
    }
    
    Active --> Cleared: /reset command
    Active --> Lost: Bot restart
    
    Cleared --> [*]
    Lost --> [*]
    
    note right of Created
        Always starts with
        system prompt
    end note
    
    note right of Trimming
        max_context_messages = 20
        System prompt preserved
    end note
    
    note right of Lost
        In-memory storage
        Data loss on restart
    end note
```

### 5.2 Message Processing State

```mermaid
stateDiagram-v2
    [*] --> Received: Message arrives
    
    Received --> TypeCheck: Check type
    
    state TypeCheck <<choice>>
    TypeCheck --> Command: starts with /
    TypeCheck --> Regular: text message
    
    state Command {
        [*] --> Parse
        Parse --> StartCmd: /start
        Parse --> HelpCmd: /help
        Parse --> ResetCmd: /reset
        Parse --> RoleCmd: /role
        Parse --> Unknown: other
        
        StartCmd --> [*]: greeting
        HelpCmd --> [*]: help text
        ResetCmd --> [*]: cleared
        RoleCmd --> [*]: prompt info
        Unknown --> [*]: null
    }
    
    state Regular {
        [*] --> GetContext
        GetContext --> AddUser
        AddUser --> CallLLM
        CallLLM --> AddAssistant
        AddAssistant --> [*]
    }
    
    Command --> Response
    Regular --> Response
    
    Response --> [*]: Send to user
```

### 5.3 Bot Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Initializing: make run
    
    Initializing --> LoadingConfig: Load .env
    LoadingConfig --> ValidatingConfig: Parse vars
    
    state ValidatingConfig <<choice>>
    ValidatingConfig --> ConfigError: Missing vars
    ValidatingConfig --> CreatingComponents: Valid
    
    ConfigError --> [*]: Exit
    
    CreatingComponents --> SetupLogging: Create instances
    SetupLogging --> StartPolling: Setup complete
    
    state StartPolling {
        [*] --> Polling
        Polling --> Polling: Check updates
        Polling --> Processing: New message
        Processing --> Polling: Done
    }
    
    StartPolling --> Stopping: Ctrl+C
    Stopping --> Cleanup: Close connections
    Cleanup --> [*]: Exit
    
    note right of Polling
        Long polling
        Telegram Bot API
    end note
```

---

## 📂 6. Структура проекта

### 6.1 Project Structure Tree

```mermaid
graph TB
    Root[systech-aidd-live/] --> Src[src/]
    Root --> Tests[tests/]
    Root --> Doc[doc/]
    Root --> Prompts[prompts/]
    Root --> Logs[logs/]
    Root --> Config[Config Files]
    
    Src --> Src1[main.py]
    Src --> Src2[config.py]
    Src --> Src3[message_handler.py]
    Src --> Src4[command_handler.py]
    Src --> Src5[llm_client.py]
    Src --> Src6[context_manager.py]
    Src --> Src7[message.py]
    Src --> Src8[protocols.py]
    Src --> Src9[exceptions.py]
    
    Tests --> Tests1[conftest.py]
    Tests --> Tests2[test_*.py x8]
    
    Doc --> Doc1[guides/]
    Doc --> Doc2[adrs/]
    Doc --> Doc3[reviews/]
    Doc --> Doc4[*.md]
    
    Doc1 --> Guides[00-visual-overview.md<br/>01-getting-started.md<br/>02-repository-tour.md<br/>03-architecture-overview.md<br/>04-data-model.md<br/>06-development-workflow.md<br/>07-testing-strategy.md<br/>08-code-review-process.md<br/>12-troubleshooting.md]
    
    Prompts --> Prompts1[system_prompt.txt]
    
    Logs --> Logs1[app.log]
    
    Config --> Config1[pyproject.toml]
    Config --> Config2[uv.lock]
    Config --> Config3[Makefile]
    Config --> Config4[.env]
    Config --> Config5[.gitignore]
    
    style Root fill:#2C3E50,stroke:#ECF0F1,stroke-width:3px,color:#ECF0F1
    style Src fill:#E74C3C,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Tests fill:#27AE60,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Doc fill:#3498DB,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Prompts fill:#9B59B6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Logs fill:#95A5A6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Config fill:#F39C12,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
```

### 6.2 Module Relationships

```mermaid
graph TD
    subgraph Core["🎯 Core"]
        main[main.py<br/>Entry Point]
        config[config.py<br/>Configuration]
    end
    
    subgraph Coordinators["🎭 Coordinators"]
        msg_handler[message_handler.py<br/>Main Coordinator]
        cmd_handler[command_handler.py<br/>Command Router]
    end
    
    subgraph Services["⚙️ Services"]
        llm[llm_client.py<br/>AI Service]
        ctx[context_manager.py<br/>State Service]
    end
    
    subgraph Foundation["🧱 Foundation"]
        message[message.py<br/>Data Model]
        protocols[protocols.py<br/>Interfaces]
        exceptions[exceptions.py<br/>Errors]
    end
    
    main --> msg_handler
    main --> config
    
    msg_handler --> cmd_handler
    msg_handler --> llm
    msg_handler --> ctx
    
    cmd_handler --> ctx
    
    llm --> message
    ctx --> message
    
    msg_handler --> protocols
    llm --> protocols
    ctx --> protocols
    
    msg_handler --> exceptions
    llm --> exceptions
    config --> exceptions
    
    style Core fill:#2C3E50,stroke:#ECF0F1,color:#ECF0F1
    style Coordinators fill:#34495E,stroke:#ECF0F1,color:#ECF0F1
    style Services fill:#2C3E50,stroke:#ECF0F1,color:#ECF0F1
    style Foundation fill:#34495E,stroke:#ECF0F1,color:#ECF0F1
    
    style main fill:#E74C3C,stroke:#ECF0F1,stroke-width:3px,color:#ECF0F1
    style msg_handler fill:#E74C3C,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style cmd_handler fill:#27AE60,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style llm fill:#9B59B6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style ctx fill:#F39C12,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
```

---

## 👤 7. User Journey

### 7.1 First-Time User Journey

```mermaid
journey
    title First-Time User Experience
    section Discovery
        Find bot in Telegram: 3: User
        Read description: 4: User
    section First Contact
        Send /start command: 5: User, Bot
        Receive greeting: 5: Bot
        Read capabilities: 4: User
    section Exploration
        Send /help: 5: User, Bot
        See available commands: 5: Bot
        Try /role command: 4: User, Bot
        Understand bot's purpose: 5: User
    section First Interaction
        Ask a question: 5: User, Bot
        Receive AI response: 5: Bot, LLM
        Bot remembers context: 5: Bot
    section Continued Use
        Ask follow-up question: 5: User, Bot
        Context maintained: 5: Bot
        Natural conversation: 5: User, Bot, LLM
```

### 7.2 Error Recovery Journey

```mermaid
journey
    title User Error Recovery Experience
    section Normal Operation
        Using bot normally: 5: User, Bot
        Getting responses: 5: Bot
    section Error Occurs
        API timeout happens: 1: LLM
        Bot catches error: 3: Bot
        User sees friendly message: 4: Bot
    section Recovery
        User waits a moment: 3: User
        Tries again: 4: User, Bot
        Success: 5: Bot, LLM
    section Context Preserved
        Conversation continues: 5: User, Bot
        Context still intact: 5: Bot
```

---

## 🛠️ 8. Процессы разработки

### 8.1 Development Workflow

```mermaid
graph TB
    Start([New Task]) --> Branch[Create<br/>Feature Branch]
    Branch --> Code[Write Code]
    Code --> Test[Write Tests]
    Test --> Format[make format]
    Format --> Lint[make lint]
    Lint --> Check{All Pass?}
    
    Check -->|No| Fix[Fix Issues]
    Fix --> Code
    
    Check -->|Yes| Coverage[make test-cov]
    Coverage --> CovCheck{Coverage<br/>100%?}
    
    CovCheck -->|No| MoreTests[Write More<br/>Tests]
    MoreTests --> Test
    
    CovCheck -->|Yes| Commit[git commit]
    Commit --> Push[git push]
    Push --> PR[Create PR]
    PR --> Review[Code Review]
    Review --> ReviewCheck{Approved?}
    
    ReviewCheck -->|No| Feedback[Address<br/>Feedback]
    Feedback --> Code
    
    ReviewCheck -->|Yes| Merge[Merge to main]
    Merge --> End([Done])
    
    style Start fill:#27AE60,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style End fill:#27AE60,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Check fill:#F39C12,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style CovCheck fill:#E67E22,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style ReviewCheck fill:#9B59B6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Merge fill:#27AE60,stroke:#ECF0F1,stroke-width:3px,color:#ECF0F1
```

### 8.2 TDD Cycle

```mermaid
graph LR
    Red[🔴 RED<br/>Write failing test] --> Green[🟢 GREEN<br/>Write minimal code]
    Green --> Blue[🔵 REFACTOR<br/>Improve code]
    Blue --> Red
    
    Red -.->|Test fails| R1[Run: make test]
    Green -.->|Test passes| G1[Run: make test]
    Blue -.->|All green| B1[Run: make check-all]
    
    style Red fill:#E74C3C,stroke:#ECF0F1,stroke-width:3px,color:#ECF0F1
    style Green fill:#27AE60,stroke:#ECF0F1,stroke-width:3px,color:#ECF0F1
    style Blue fill:#3498DB,stroke:#ECF0F1,stroke-width:3px,color:#ECF0F1
```

### 8.3 Testing Strategy

```mermaid
graph TB
    Tests[Test Suite] --> Unit[Unit Tests<br/>29 tests]
    Tests --> Integration[Integration Tests<br/>1 test]
    
    Unit --> Fast[⚡ Fast<br/>~2.8s]
    Unit --> Isolated[🔒 Isolated<br/>Mocked deps]
    Unit --> Coverage[📊 Coverage<br/>100%]
    
    Integration --> Slow[🐢 Slower<br/>~4.5s]
    Integration --> Real[🌐 Real APIs<br/>Actual calls]
    Integration --> E2E[🔗 End-to-End<br/>Full flow]
    
    style Tests fill:#2C3E50,stroke:#ECF0F1,stroke-width:3px,color:#ECF0F1
    style Unit fill:#27AE60,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Integration fill:#3498DB,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
```

---

## ⚠️ 9. Error Handling

### 9.1 Error Propagation

```mermaid
graph TB
    Start[Error Occurs] --> Where{Where?}
    
    Where -->|Config| ConfigErr[ConfigError]
    Where -->|LLM API| LLMErr[LLMError]
    Where -->|Other| GenErr[Exception]
    
    ConfigErr --> Exit[Exit Application<br/>with error message]
    
    LLMErr --> Log1[Log error<br/>with details]
    GenErr --> Log2[Log exception<br/>with stack trace]
    
    Log1 --> User1[Send user<br/>friendly message]
    Log2 --> User2[Send generic<br/>error message]
    
    User1 --> Continue[Continue<br/>processing]
    User2 --> Continue
    
    style Start fill:#E74C3C,stroke:#ECF0F1,stroke-width:3px,color:#ECF0F1
    style ConfigErr fill:#E67E22,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style LLMErr fill:#E67E22,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style GenErr fill:#95A5A6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Exit fill:#C0392B,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Continue fill:#27AE60,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
```

### 9.2 Retry Strategy (Future)

```mermaid
graph LR
    Request[API Request] --> Try{Try}
    Try --> Success{Success?}
    
    Success -->|Yes| Return[Return Response]
    Success -->|No| Count{Retry<br/>Count?}
    
    Count -->|< Max| Wait[Wait<br/>Backoff]
    Wait --> Try
    
    Count -->|>= Max| Fail[Raise Error]
    
    style Request fill:#3498DB,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Return fill:#27AE60,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Fail fill:#E74C3C,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Wait fill:#F39C12,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
```

---

## 📅 10. История проекта

### 10.1 Development Timeline

```mermaid
gantt
    title Разработка проекта (8 итераций)
    dateFormat YYYY-MM-DD
    section MVP Phase
    Итерация 0 Echo-бот           :2025-10-10, 1d
    Итерация 1 Интеграция LLM      :2025-10-10, 1d
    Итерация 2 История диалога     :2025-10-10, 1d
    Итерация 3 Команды и обрезка   :2025-10-10, 1d
    Итерация 4 Финальное тестиров  :2025-10-10, 1d
    section Tech Debt Phase
    Итерация 0 Инструменты качества :2025-10-11, 1d
    Итерация 1 Type hints + validat :2025-10-11, 1d
    Итерация 2 Архитектурный рефакт :2025-10-11, 1d
    Итерация 3 Улучшение тестирован :2025-10-11, 1d
    Итерация 4 Финальная проверка   :2025-10-11, 1d
```

### 10.2 Architecture Evolution

```mermaid
graph LR
    subgraph MVP["MVP v0.1"]
        M1[Echo Bot<br/>Simple]
    end
    
    subgraph MVP2["MVP v0.2"]
        M2[+ LLM<br/>Integration]
    end
    
    subgraph MVP3["MVP v0.3"]
        M3[+ Context<br/>Management]
    end
    
    subgraph MVP4["MVP v1.0"]
        M4[+ Commands<br/>Complete]
    end
    
    subgraph Refactor["Refactored v2.0"]
        R1[+ Type Safety<br/>+ SOLID<br/>+ 100% Coverage]
    end
    
    MVP --> MVP2
    MVP2 --> MVP3
    MVP3 --> MVP4
    MVP4 --> Refactor
    
    style MVP fill:#95A5A6,stroke:#ECF0F1,color:#ECF0F1
    style MVP2 fill:#3498DB,stroke:#ECF0F1,color:#ECF0F1
    style MVP3 fill:#F39C12,stroke:#ECF0F1,color:#ECF0F1
    style MVP4 fill:#9B59B6,stroke:#ECF0F1,color:#ECF0F1
    style Refactor fill:#27AE60,stroke:#ECF0F1,stroke-width:3px,color:#ECF0F1
```

### 10.3 Quality Metrics Evolution

```mermaid
graph TB
    Start[Start MVP] --> M1[Coverage: 0%<br/>Type hints: 0%<br/>Tests: 0]
    M1 --> M2[Coverage: 43%<br/>Type hints: 0%<br/>Tests: 4]
    M2 --> M3[Coverage: 47%<br/>Type hints: 100%<br/>Tests: 4]
    M3 --> M4[Coverage: 42%<br/>Type hints: 100%<br/>Tests: 4]
    M4 --> Final[Coverage: 100%<br/>Type hints: 100%<br/>Tests: 30]
    
    style Start fill:#95A5A6,stroke:#ECF0F1,stroke-width:2px,color:#ECF0F1
    style Final fill:#27AE60,stroke:#ECF0F1,stroke-width:3px,color:#ECF0F1
```

---

## 🎯 Резюме визуализаций

### Ключевые точки зрения:

1. **Системная** - как компоненты связаны
2. **Структурная** - классы и их отношения
3. **Динамическая** - потоки данных и взаимодействий
4. **Процессная** - lifecycle и state machines
5. **Организационная** - структура файлов и модулей
6. **Пользовательская** - user journey
7. **Разработческая** - workflow и TDD
8. **Историческая** - эволюция проекта

### Использованные типы диаграмм:

- ✅ **Graph** - архитектура, зависимости, flows
- ✅ **Sequence** - взаимодействия, API calls
- ✅ **State** - жизненные циклы
- ✅ **Class** - структура классов
- ✅ **Journey** - пользовательский опыт
- ✅ **Gantt** - timeline разработки

---

## 📚 Связанные гайды

Для детального понимания см:
- [Architecture Overview](03-architecture-overview.md) - текстовые объяснения
- [Data Model](04-data-model.md) - детали структур данных
- [Development Workflow](06-development-workflow.md) - процесс разработки
- [Getting Started](01-getting-started.md) - начало работы

---

**💡 Совет**: Сохраните этот гайд как визуальный справочник. Диаграммы обновляются вместе с проектом.

