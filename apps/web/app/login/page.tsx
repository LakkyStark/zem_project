"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { login } from "@/lib/api";
import { setToken } from "@/lib/auth";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      const t = await login(email, password);
      setToken(t.access_token);
      router.push("/organizations");
    } catch (err: any) {
      const detail = err?.detail ? String(err.detail) : null;
      const status = err?.status ? ` (${err.status})` : "";
      setError(detail ?? `Не удалось войти${status}`);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="bg-grid">
      <main className="mx-auto flex max-w-md flex-col gap-8 px-6 py-16">
        <header className="space-y-2">
          <p className="text-sm font-medium tracking-wide text-emerald-300/90">BuildLaw AI</p>
          <h1 className="text-3xl font-semibold tracking-tight">Вход</h1>
          <p className="text-slate-300">Продолжите работу с документами вашей организации.</p>
        </header>

        <Card className="p-6">
          <form onSubmit={onSubmit} className="space-y-4">
            <Input
              label="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              type="email"
              required
            />
            <Input
              label="Пароль"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              type="password"
              required
            />

            {error ? <p className="text-sm text-red-300">{error}</p> : null}

            <Button className="w-full" type="submit" disabled={busy}>
              {busy ? "Входим..." : "Войти"}
            </Button>
          </form>
        </Card>

        <p className="text-sm text-slate-300">
          Нет аккаунта?{" "}
          <Link className="text-emerald-400 underline" href="/register">
            Регистрация
          </Link>
        </p>
      </main>
    </div>
  );
}

