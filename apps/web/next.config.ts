import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // macOS часто упирается в лимит file watchers (EMFILE). Polling проще и стабильнее для MVP.
  webpack: (config) => {
    config.watchOptions = {
      ...(config.watchOptions ?? {}),
      poll: 1000,
      aggregateTimeout: 300,
    };
    return config;
  },
};

export default nextConfig;

import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
};

export default nextConfig;
