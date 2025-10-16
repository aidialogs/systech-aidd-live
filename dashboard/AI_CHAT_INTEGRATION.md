# AI Chat Component Integration Guide

## ✅ Installation Complete

### What Was Done

1. **Dependency Installed:**
   ```bash
   pnpm add framer-motion
   ```
   - `lucide-react` was already installed ✅
   - `framer-motion` v12.23.24 added ✅

2. **Component Created:**
   - `components/ui/ai-chat.tsx` - Main AI chat component
   - `app/chat-demo/page.tsx` - Demo page

3. **Project Setup Verified:**
   - ✅ shadcn configured correctly (`components.json`)
   - ✅ Tailwind CSS v4 configured
   - ✅ TypeScript strict mode enabled
   - ✅ Path aliases properly set (`@/components`, `@/lib/utils`)

---

## 📋 Component Analysis

### Component Structure

```tsx
<AIChatCard className?: string />
```

### Props
- `className` (optional): Additional CSS classes for customization

### Internal State
```typescript
messages: { sender: "ai" | "user"; text: string }[]  // Message history
input: string                                          // Current input value
isTyping: boolean                                      // AI typing indicator
```

### Features
- ✨ Animated rotating border
- 🎨 Gradient background with floating particles
- 💬 Message bubbles with smooth animations
- ⌨️ Typing indicator for AI responses
- 📱 Fixed size: 360px × 460px (customizable via className)

---

## 🎯 Integration Questions & Answers

### 1. What data/props will be passed to this component?

**Current Implementation:**
- Component is self-contained with local state
- No external props required (except optional `className`)

**Recommended Enhancement:**
```typescript
interface AIChatCardProps {
  className?: string;
  initialMessages?: { sender: "ai" | "user"; text: string }[];
  onSendMessage?: (message: string) => Promise<string>;
  apiEndpoint?: string;
  userId?: string;
}
```

### 2. State Management Requirements

**Current:**
- Uses React `useState` for local state
- Simulated AI responses with `setTimeout`

**For Production:**
- Connect to your backend API (e.g., `/api/chat`)
- Consider using:
  - `useSWR` for data fetching
  - `react-query` for mutations
  - WebSocket for real-time responses

**Example Integration with Your API:**
```typescript
import { useState } from "react";

const handleSend = async () => {
  if (!input.trim()) return;
  
  setMessages([...messages, { sender: "user", text: input }]);
  setInput("");
  setIsTyping(true);

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: input })
    });
    
    const data = await response.json();
    setMessages((prev) => [...prev, { sender: "ai", text: data.response }]);
  } catch (error) {
    setMessages((prev) => [...prev, { 
      sender: "ai", 
      text: "Sorry, I encountered an error." 
    }]);
  } finally {
    setIsTyping(false);
  }
};
```

### 3. Required Assets

**Icons:**
- ✅ `Send` icon from `lucide-react` (already imported)
- No additional images needed

**Fonts:**
- Uses system fonts (inherited from Tailwind)

**Optional Enhancements:**
- Add bot avatar using `lucide-react` icons (e.g., `Bot`, `MessageSquare`)
- User avatar could use your existing `@/components/ui/avatar` component

### 4. Responsive Behavior

**Current:**
- Fixed size: `w-[360px] h-[460px]`
- Not responsive by default

**Recommendations for Mobile:**
```tsx
// Option 1: Full screen on mobile
className="w-full h-full md:w-[360px] md:h-[460px]"

// Option 2: Responsive sizing
className="w-[90vw] max-w-[360px] h-[70vh] max-h-[460px]"

// Option 3: Drawer on mobile (using vaul)
import { Drawer } from "@/components/ui/drawer"
```

### 5. Best Place to Use in Your App

Based on your dashboard structure, here are the recommended placements:

#### **Option A: Floating Chat Button (Recommended)**
Add a floating action button that opens the chat in a modal/drawer:

```tsx
// dashboard/components/floating-chat-button.tsx
"use client";

import { useState } from "react";
import { MessageSquare, X } from "lucide-react";
import AIChatCard from "@/components/ui/ai-chat";
import { motion, AnimatePresence } from "framer-motion";

export function FloatingChatButton() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Chat button */}
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 z-50 p-4 rounded-full bg-primary text-primary-foreground shadow-lg hover:shadow-xl transition-shadow"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
      >
        {isOpen ? <X className="w-6 h-6" /> : <MessageSquare className="w-6 h-6" />}
      </motion.button>

      {/* Chat card */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 20 }}
            className="fixed bottom-24 right-6 z-40"
          >
            <AIChatCard />
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
```

Then add to your dashboard layout:
```tsx
// dashboard/app/dashboard/page.tsx
import { FloatingChatButton } from "@/components/floating-chat-button"

export default function Page() {
  // ... existing code
  return (
    <SidebarProvider>
      {/* ... existing layout */}
      <FloatingChatButton />
    </SidebarProvider>
  )
}
```

#### **Option B: Sidebar Navigation Item**
Add to your sidebar navigation:

```tsx
// dashboard/components/app-sidebar.tsx
import { MessageSquare } from "lucide-react";

// Add to nav items:
{
  title: "AI Assistant",
  url: "/chat-demo",
  icon: MessageSquare,
}
```

#### **Option C: Dashboard Page Section**
Add as a widget in the dashboard:

```tsx
// dashboard/app/dashboard/page.tsx
<div className="px-4 lg:px-6">
  <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
    <SectionCards overview={data.overview} />
    <div className="flex items-center justify-center">
      <AIChatCard className="w-full max-w-md" />
    </div>
  </div>
</div>
```

---

## 🚀 Quick Start

### 1. View the Demo
Start the development server and visit the demo page:

```bash
cd dashboard
pnpm dev
```

Visit: `http://localhost:3000/chat-demo`

### 2. Import and Use

```tsx
import AIChatCard from "@/components/ui/ai-chat";

export default function YourPage() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <AIChatCard />
    </div>
  );
}
```

### 3. Customize Styling

```tsx
<AIChatCard className="w-full h-screen md:w-[400px] md:h-[600px]" />
```

---

## 🔧 Production Enhancements

### Connect to Real API

1. Create API route:
```typescript
// dashboard/app/api/chat/route.ts
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const { message } = await request.json();
  
  // Call your AI service (OpenAI, Anthropic, etc.)
  const response = await fetch('YOUR_AI_SERVICE_URL', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });
  
  const data = await response.json();
  return NextResponse.json({ response: data.message });
}
```

2. Update component to use API (see State Management section above)

### Add Message Persistence

```typescript
// Save to localStorage
useEffect(() => {
  localStorage.setItem('chat-messages', JSON.stringify(messages));
}, [messages]);

// Load from localStorage
useEffect(() => {
  const saved = localStorage.getItem('chat-messages');
  if (saved) setMessages(JSON.parse(saved));
}, []);
```

### Add User Context

For your Telegram bot dashboard, you could integrate bot statistics:

```typescript
interface Message {
  sender: "ai" | "user";
  text: string;
  metadata?: {
    userId?: string;
    timestamp?: Date;
    context?: "dashboard" | "bot";
  };
}
```

---

## 📱 Responsive Design Tips

```tsx
// Mobile-first responsive design
<div className="
  fixed bottom-0 right-0 
  w-full h-[100dvh]                    // Full screen mobile
  md:relative md:w-[360px] md:h-[460px] // Fixed size desktop
  md:rounded-2xl                        // Rounded on desktop
">
  <AIChatCard className="w-full h-full" />
</div>
```

---

## 🎨 Theme Integration

The component uses a dark theme by default. To integrate with your app's theme:

```tsx
// Use CSS variables from your theme
<div className="
  bg-background                        // Use theme background
  text-foreground                      // Use theme text color
  border-border                        // Use theme border color
">
```

---

## ✅ Type Checking

Verify TypeScript compilation:
```bash
cd dashboard
pnpm type-check
```

---

## 🐛 Common Issues

### Issue: Animations not working
**Solution:** Ensure `framer-motion` is installed:
```bash
pnpm add framer-motion
```

### Issue: `cn` function not found
**Solution:** Check `lib/utils.ts` exists with:
```typescript
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### Issue: Import paths not working
**Solution:** Verify `tsconfig.json` has path aliases:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

---

## 📚 Next Steps

1. ✅ Component installed and working
2. 🔲 Choose integration approach (floating button, sidebar, or page)
3. 🔲 Connect to real AI API endpoint
4. 🔲 Add message persistence
5. 🔲 Customize styling for your brand
6. 🔲 Add user authentication context
7. 🔲 Implement responsive design
8. 🔲 Add error handling and loading states

---

## 🤝 Support

For issues or questions:
- Component source: `components/ui/ai-chat.tsx`
- Demo page: `app/chat-demo/page.tsx`
- Original component: [21st.dev](https://21st.dev/r/beratberkayg/ai-chat)

