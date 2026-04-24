"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { apiFetch, login } from "@/lib/api";
import { setToken } from "@/lib/auth";

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
    <main className="mx-auto flex max-w-md flex-col gap-8 px-6 py-16">
      <header className="space-y-2">
        <h1 className="text-3xl font-semibold tracking-tight">Регистрация</h1>
        <p className="text-slate-300">Создайте аккаунт и организацию</p>
      </header>

      <form onSubmit={onSubmit} className="space-y-4 rounded-xl border border-slate-800 bg-slate-900/60 p-6">
        <label className="block space-y-2">
          <span className="text-sm text-slate-300">Название организации</span>
          <input
            className="w-full rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 text-slate-100"
            value={orgName}
            onChange={(e) => setOrgName(e.target.value)}
            required
          />
        </label>
        <label className="block space-y-2">
          <span className="text-sm text-slate-300">Email</span>
          <input
            className="w-full rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 text-slate-100"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            type="email"
            required
          />
        </label>
        <label className="block space-y-2">
          <span className="text-sm text-slate-300">Имя (опционально)</span>
          <input
            className="w-full rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 text-slate-100"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
          />
        </label>
        <label className="block space-y-2">
          <span className="text-sm text-slate-300">Пароль</span>
          <input
            className="w-full rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 text-slate-100"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            minLength={8}
            required
          />
        </label>

        {error ? <p className="text-sm text-red-300">{error}</p> : null}

        <button
          disabled={busy}
          className="w-full rounded-lg bg-emerald-500 px-4 py-2 font-medium text-slate-950 disabled:opacity-60"
          type="submit"
        >
          {busy ? "Создаём..." : "Создать аккаунт"}
        </button>
      </form>

      <p className="text-sm text-slate-300">
        Уже есть аккаунт?{" "}
        <Link className="text-emerald-400 underline" href="/login">
          Войти
        </Link>
      </p>
    </main>
  );
}

