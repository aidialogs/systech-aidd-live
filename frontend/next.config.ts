import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Standalone output для оптимизации Docker образа
  output: "standalone",
};

export default nextConfig;
