"use client";

import { motion } from "framer-motion";

export function TypingIndicator() {
  return (
    <motion.div
      className="flex items-center gap-1 px-3 py-2 rounded-xl max-w-[30%] bg-white/10 self-start"
      initial={{ opacity: 0 }}
      animate={{ opacity: [0, 1, 0.6, 1] }}
      transition={{ repeat: Infinity, duration: 1.2 }}
    >
      <span className="w-2 h-2 rounded-full bg-white animate-pulse"></span>
      <span className="w-2 h-2 rounded-full bg-white animate-pulse delay-200"></span>
      <span className="w-2 h-2 rounded-full bg-white animate-pulse delay-400"></span>
    </motion.div>
  );
}

