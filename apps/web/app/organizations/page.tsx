"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { apiFetch } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

type OrganizationSummary = { id: string; name: string; role: string };

export default function OrganizationsPage() {
  const [items, setItems] = useState<OrganizationSummary[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await apiFetch<OrganizationSummary[]>("/v1/organizations/");
        if (active) setItems(data);
      } catch (e: any) {
        if (active) setError(e?.detail ?? "Не удалось загрузить организации");
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => {
      active = false;
    };
  }, []);

  return (
    <div className="bg-grid">
      <main className="mx-auto flex max-w-4xl flex-col gap-10 px-6 py-16">
        <header className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div className="space-y-2">
            <p className="text-sm font-medium tracking-wide text-emerald-300/90">BuildLaw AI</p>
            <h1 className="text-3xl font-semibold tracking-tight">Организации</h1>
            <p className="text-slate-300">Выберите организацию, чтобы работать с документами.</p>
          </div>
          <div className="flex items-center gap-2">
            <Button href="/login" variant="ghost">
              Войти другим аккаунтом
            </Button>
          </div>
        </header>

        {loading ? <p className="text-slate-300">Загрузка...</p> : null}
        {error ? <p className="text-sm text-red-300">{error}</p> : null}

        {!loading && !error && items.length === 0 ? (
          <Card className="p-8 text-slate-300">
            Пока нет организаций (обычно создаётся при регистрации).
          </Card>
        ) : null}

        <div className="grid gap-3">
          {items.map((o) => (
            <Link
              key={o.id}
              href={`/organizations/${o.id}/documents`}
              className="rounded-2xl border border-slate-800 bg-slate-900/55 p-5 hover:border-emerald-700/50"
            >
              <div className="flex items-center justify-between gap-4">
                <div className="min-w-0">
                  <div className="truncate text-lg font-medium text-white">{o.name}</div>
                  <div className="text-sm text-slate-400">роль: {o.role}</div>
                </div>
                <span className="text-emerald-400">→</span>
              </div>
            </Link>
          ))}
        </div>
      </main>
    </div>
  );
}

