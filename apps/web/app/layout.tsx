import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BuildLaw AI",
  description: "AI SaaS для анализа строительных и земельно-правовых документов",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru">
      <body className="font-sans">{children}</body>
    </html>
  );
}
