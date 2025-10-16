# systech-aidd Dashboard

Frontend application for systech-aidd AI Bot Statistics Dashboard.

## Tech Stack

- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript (strict mode)
- **Styling:** Tailwind CSS 4.x
- **UI Components:** shadcn/ui (Radix UI + Tailwind)
- **Package Manager:** pnpm
- **Code Quality:** ESLint + Prettier

## Getting Started

### Prerequisites

- Node.js 18+
- pnpm 9+
- Backend API running on `http://localhost:8000`

### Installation

```bash
pnpm install
```

### Development

```bash
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Building

```bash
pnpm build
```

### Linting & Formatting

```bash
# Run ESLint
pnpm lint

# Fix ESLint errors
pnpm lint:fix

# Format code with Prettier
pnpm format

# Check formatting
pnpm format:check

# TypeScript type checking
pnpm type-check
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Dashboard page
│   └── globals.css        # Global styles
├── components/
│   ├── ui/                # shadcn/ui components
│   ├── dashboard/         # Dashboard components
│   └── layout/            # Layout components
├── lib/
│   ├── api.ts            # API client
│   ├── utils.ts          # Utility functions
│   └── types.ts          # TypeScript types
├── doc/                   # Documentation
├── public/                # Static assets
└── ...config files
```

## Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Documentation

- [Frontend Vision](./doc/front-vision.md) - Technical vision and architecture
- [Dashboard Requirements](./doc/dashboard-requirements.md) - Dashboard requirements
- [Frontend Roadmap](./doc/frontend-roadmap.md) - Development roadmap
- [ADR-07](../doc/adrs/ADR-07.md) - Technology stack decision record

## Sprint Status

**Sprint S2: Scaffolding** - ✅ Completed

- ✅ Next.js project initialization
- ✅ TypeScript strict mode configuration
- ✅ Prettier and ESLint setup
- ✅ shadcn/ui integration
- ✅ Project structure creation
- ✅ Type definitions
- ✅ Base layout and page stub

**Next: Sprint S3** - Dashboard implementation with MockAPI integration

## License

Private project for systech-aidd
