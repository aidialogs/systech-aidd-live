# ⚡ 30-Second Onboarding Guide

**Цель**: Запустить проект за 30 секунд (если у вас уже есть Python, Docker и токены).

---

## Prerequisites

- ✅ Python 3.11+
- ✅ Docker Desktop запущен
- ✅ Telegram bot token (от @BotFather)
- ✅ OpenRouter API key

---

## Quick Start

```bash
# 1. Clone & install (10 sec)
git clone <repo-url> systech-aidd-live && cd systech-aidd-live
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --extra dev

# 2. Configure (5 sec)
cp .env.example .env
# Edit .env: add your BOT_TOKEN and LLM_API_KEY

# 3. Start database (5 sec)
make db-up
make db-migrate

# 4. Run bot (10 sec)
make run
```

**Done!** Open Telegram and message your bot `/start`

---

## Optional: Run API + Frontend

```bash
# Terminal 1: API
make api-run

# Terminal 2: Frontend
make frontend-dev

# Open http://localhost:3000
```

---

## What's Next?

➡️ Read full guides: [doc/guides/README.md](README.md)

**Must read**: [GUIDE-01](01-getting-started.md) → [GUIDE-02](02-architecture.md) → [GUIDE-06](06-codebase-tour.md)
