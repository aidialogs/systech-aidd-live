'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { FloatingChatButton } from '@/components/chat/floating-chat-button';

export default function HomePage() {
  return (
    <>
      <div className="flex min-h-[calc(100vh-3.5rem)] items-center justify-center p-8 pb-24">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>SYSTECH AIDD</CardTitle>
            <CardDescription>
              AI-powered Telegram bot analytics and chat
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            <Button asChild>
              <Link href="/dashboard">Open Dashboard</Link>
            </Button>
            <Button asChild variant="outline">
              <Link href="/chat">Admin Chat</Link>
            </Button>
          </CardContent>
        </Card>
      </div>

      <FloatingChatButton />
    </>
  );
}
