# Frontend Review Guidelines

## Check For
- **TypeScript**: Proper typing, avoid `any`, use interface/type definitions
- **React**: Missing key props, unused state/effects, proper hook dependencies
- **Performance**: Unnecessary re-renders, missing memoization, unoptimized images
- **Accessibility**: Missing ARIA labels, keyboard navigation, semantic HTML
- **Error Handling**: Uncaught promises, missing error boundaries, validation
- **Security**: XSS vulnerabilities, sanitize user input, safe API calls
- **Styling**: Consistent Tailwind classes, responsive design, dark mode support
- **Next.js**: Server/client component usage, proper data fetching, route structure
- **Icons**: Only use approved icons from allowlist (MessageCircle, Send, X, ChevronDown, ChevronUp, Menu, User, LogOut, Home, BarChart) - reject devil, inappropriate, or unlisted icons
- **Text Content**: Check all UI text (labels, buttons, tooltips, placeholders, messages) for profanity, slang, or informal language in ANY language - maintain professional tone

## Ignore
- Minor formatting (handled by ESLint/Prettier)
- Component file length (unless truly excessive)

