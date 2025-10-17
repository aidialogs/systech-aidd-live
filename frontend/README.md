# SYSTECH AIDD Frontend

Modern web dashboard and admin chat interface for AI-powered Telegram bot analytics.

## Tech Stack

- **Framework**: Next.js 15+ (App Router)
- **Language**: TypeScript 5+
- **UI Library**: shadcn/ui
- **Styling**: Tailwind CSS
- **Package Manager**: pnpm
- **Icons**: lucide-react
- **Themes**: next-themes (dark/light/system)

## Getting Started

### Prerequisites

- Node.js 18+
- pnpm 8+

### Installation

```bash
pnpm install
```

### Development

```bash
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

```bash
pnpm build
pnpm start
```

### Code Quality

```bash
pnpm lint           # Run ESLint
pnpm format         # Format with Prettier
pnpm type-check     # TypeScript type checking
```

## Project Structure

```
src/
├── app/              # Next.js App Router pages
├── components/
│   ├── ui/           # shadcn/ui components
│   ├── dashboard/    # Dashboard components
│   ├── chat/         # Chat components
│   └── shared/       # Shared components (Header, ThemeToggle)
├── lib/              # Utilities and helpers
│   ├── api.ts        # API client
│   ├── types.ts      # TypeScript types
│   └── utils.ts      # Utility functions
└── config/           # Configuration
    └── site.ts       # Site config
```

## Environment Variables

Copy `.env.local.example` to `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Features

- 📊 **Dashboard**: Real-time statistics and analytics (Sprint S3)
- 💬 **Admin Chat**: AI-powered chat interface (Sprint S4)
- 🎨 **Modern UI**: Built with shadcn/ui and Tailwind CSS
- 🌓 **Dark Mode**: Light/Dark/System theme support
- 📱 **Responsive**: Mobile-friendly design
- ⚡ **Fast**: Next.js App Router with Server Components

## Documentation

- [Frontend Vision](doc/frontend-vision.md)
- [Frontend Roadmap](doc/frontend-roadmap.md)
- [Sprint Plans](doc/plans/)

## Sprint S3: Dashboard Implementation

The Dashboard is now fully implemented with:

- ✅ 4 Overview metric cards (Total Messages, Users, Active Chats, Avg Length)
- ✅ Messages Over Time chart (Area chart with gradient)
- ✅ Messages by Role chart (Bar chart for User/Assistant/System)
- ✅ Quick Metrics card (Top KPIs)
- ✅ Period selector (Day/Week/Month/All Time)
- ✅ Full API integration with Mock API
- ✅ Colorful, vibrant design
- ✅ Responsive layout for all devices
- ✅ Dark/Light theme support

### Running the Dashboard

**Option 1: Run both API and Frontend together**

From the project root:

```bash
make dev
```

This starts both:
- API server at http://localhost:8000
- Frontend at http://localhost:3000

**Option 2: Run separately**

Terminal 1 - Backend API:
```bash
make api-run
```

Terminal 2 - Frontend:
```bash
make frontend-dev
# or from frontend/ directory:
cd frontend && pnpm dev
```

Then open [http://localhost:3000/dashboard](http://localhost:3000/dashboard)

### Dashboard Features

1. **Period Filtering**: Switch between Day/Week/Month/All Time
2. **Real-time Data**: Fetches from Mock API (will use real DB in Sprint S5)
3. **Responsive Design**: Adapts to mobile/tablet/desktop
4. **Theme Support**: Works in both light and dark modes
5. **Error Handling**: Shows helpful messages if API is unavailable

## Backend API

Backend API runs on `http://localhost:8000`:

- `GET /api/v1/statistics?period={day|week|month|all}` - Statistics data

See [API examples](../doc/api-examples.md) for details.
