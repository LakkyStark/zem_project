"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { apiFetch, login } from "@/lib/api";
import { setToken } from "@/lib/auth";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";

type RegisterRequest = {
  email: string;
  password: string;
  full_name?: string | null;
  organization_name: string;
};

export default function RegisterPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [orgName, setOrgName] = useState("Моя организация");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      const payload: RegisterRequest = {
        email,
        password,
        full_name: fullName ? fullName : null,
        organization_name: orgName,
      };
      await apiFetch("/v1/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        skipAuth: true,
      });
      const t = await login(email, password);
      setToken(t.access_token);
      router.push("/organizations");
    } catch (err: any) {
      setError(err?.detail ?? "Не удалось зарегистрироваться");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="bg-grid">
      <main className="mx-auto flex max-w-md flex-col gap-8 px-6 py-16">
        <header className="space-y-2">
          <p className="text-sm font-medium tracking-wide text-emerald-300/90">BuildLaw AI</p>
          <h1 className="text-3xl font-semibold tracking-tight">Регистрация</h1>
          <p className="text-slate-300">Создайте аккаунт и организацию — займёт меньше минуты.</p>
        </header>

        <Card className="p-6">
          <form onSubmit={onSubmit} className="space-y-4">
            <Input
              label="Название организации"
              value={orgName}
              onChange={(e) => setOrgName(e.target.value)}
              required
            />
            <Input
              label="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              type="email"
              required
            />
            <Input
              label="Имя (опционально)"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
            />
            <Input
              label="Пароль"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              type="password"
              minLength={8}
              required
            />

            {error ? <p className="text-sm text-red-300">{error}</p> : null}

            <Button className="w-full" type="submit" disabled={busy}>
              {busy ? "Создаём..." : "Создать аккаунт"}
            </Button>
          </form>
        </Card>

        <p className="text-sm text-slate-300">
          Уже есть аккаунт?{" "}
          <Link className="text-emerald-400 underline" href="/login">
            Войти
          </Link>
        </p>
      </main>
    </div>
  );
}

