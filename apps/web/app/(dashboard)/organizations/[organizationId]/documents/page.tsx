"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { apiFetch } from "@/lib/api";
import { DocumentStatus, StatusBadge } from "@/lib/documentStatus";

type DocumentListItem = {
  id: string;
  type: string;
  original_filename: string;
  status: DocumentStatus;
  pages_count: number;
  created_at: string;
};

type DocumentListResponse = { items: DocumentListItem[]; next_cursor: string | null };

export default function DocumentsListPage() {
  const params = useParams<{ organizationId: string }>();
  const orgId = params.organizationId;
  const [data, setData] = useState<DocumentListResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await apiFetch<DocumentListResponse>(`/v1/organizations/${orgId}/documents?limit=50`);
        if (active) setData(res);
      } catch (e: any) {
        if (active) setError(e?.detail ?? "Не удалось загрузить документы");
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => {
      active = false;
    };
  }, [orgId]);

  return (
    <main className="space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">Документы</h1>
          <p className="text-slate-300">Загрузки и статус OCR/анализа.</p>
        </div>
        <Link
          href={`/organizations/${orgId}/documents/upload`}
          className="rounded-lg bg-emerald-500 px-4 py-2 font-medium text-slate-950"
        >
          Загрузить документ
        </Link>
      </div>

      {loading ? <p className="text-slate-300">Загрузка...</p> : null}
      {error ? <p className="text-sm text-red-300">{error}</p> : null}

      {!loading && !error && (data?.items?.length ?? 0) === 0 ? (
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-6 text-slate-300">
          Пока нет документов. Нажмите «Загрузить документ».
        </div>
      ) : null}

      {data?.items?.length ? (
        <div className="overflow-hidden rounded-xl border border-slate-800">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-950/80 text-slate-300">
              <tr>
                <th className="px-4 py-3 font-medium">Файл</th>
                <th className="px-4 py-3 font-medium">Тип</th>
                <th className="px-4 py-3 font-medium">Статус</th>
                <th className="px-4 py-3 font-medium">Страниц</th>
                <th className="px-4 py-3 font-medium">Создан</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 bg-slate-900/60">
              {data.items.map((d) => (
                <tr key={d.id} className="hover:bg-slate-900">
                  <td className="px-4 py-3">
                    <Link
                      className="text-emerald-400 underline"
                      href={`/organizations/${orgId}/documents/${d.id}`}
                    >
                      {d.original_filename}
                    </Link>
                  </td>
                  <td className="px-4 py-3 text-slate-200">{d.type}</td>
                  <td className="px-4 py-3">
                    <StatusBadge status={d.status} />
                  </td>
                  <td className="px-4 py-3 text-slate-200">{d.pages_count}</td>
                  <td className="px-4 py-3 text-slate-300">
                    {new Date(d.created_at).toLocaleString("ru-RU")}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
    </main>
  );
}

