"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import type { ChatMessage } from "@/types/api";

interface MessageItemProps {
  message: ChatMessage;
  showSqlQuery?: boolean;
}

export function MessageItem({ message, showSqlQuery }: MessageItemProps) {
  const isUser = message.role === "user";
  const isSystem = message.role === "system";

  // Don't render system messages
  if (isSystem) {
    return null;
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className={cn(
        "px-3 py-2 rounded-xl max-w-[80%] shadow-md backdrop-blur-md",
        isUser
          ? "bg-white/30 text-black font-semibold self-end"
          : "bg-white/10 text-white self-start"
      )}
    >
      <div>{message.content}</div>
      {showSqlQuery && message.sql_query && (
        <div className="mt-2 pt-2 border-t border-white/20">
          <div className="text-xs text-white/60 mb-1">SQL Query:</div>
          <pre className="text-xs bg-black/30 p-2 rounded overflow-x-auto">
            {message.sql_query}
          </pre>
        </div>
      )}
    </motion.div>
  );
}

