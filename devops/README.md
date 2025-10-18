# DevOps Directory

This directory contains Docker and deployment infrastructure for the AIDD Live project.

## Current Status

**Project Phase:** MVP - Telegram Bot Only

The project is currently in MVP phase with only the Telegram bot component. Future sprints will add FastAPI backend and Next.js frontend.

## Contents

- `doc/devops-roadmap.md` - DevOps development roadmap and sprint planning

## Planned Structure

```
devops/
├── README.md                    # This file
├── doc/
│   └── devops-roadmap.md        # DevOps sprints roadmap
├── Dockerfile.bot               # (Planned) Docker image for Telegram bot
├── docker-compose.yml           # (Planned) Production orchestration
├── docker-compose.dev.yml       # (Planned) Development overrides
└── .hadolint.yaml              # (Planned) Dockerfile linter config
```

## Next Steps

See `doc/devops-roadmap.md` for the complete DevOps roadmap including:
- **Sprint D1:** Docker Image for Bot & Best Practices (Planned)
- **Sprint D2:** CI Pipeline Setup (Planned)
- **Sprint D3:** CD Pipeline & Deployment (Planned)

## Documentation

- [DevOps Roadmap](doc/devops-roadmap.md) - Complete roadmap with sprint details
- [Project Vision](../doc/vision.md) - Technical vision document
- [Main README](../README.md) - Project overview and quick start

---

Last Updated: 2025-10-18
