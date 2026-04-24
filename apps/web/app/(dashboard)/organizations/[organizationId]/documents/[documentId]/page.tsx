"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";

import { apiFetch } from "@/lib/api";
import { DocumentStatus, StatusBadge, statusMeta } from "@/lib/documentStatus";
import { Card } from "@/components/ui/Card";

type DocumentPage = { page_number: number; ocr_text: string; confidence: number };
type DocumentDetails = {
  id: string;
  type: string;
  original_filename: string;
  status: DocumentStatus;
  pages_count: number;
  created_at: string;
  error_message?: string | null;
  pages: DocumentPage[];
};

export default function DocumentDetailsPage({
}: {}) {
  const params = useParams<{ organizationId: string; documentId: string }>();
  const orgId = params.organizationId;
  const docId = params.documentId;

  const [data, setData] = useState<DocumentDetails | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const shouldPoll = useMemo(() => {
    if (!data) return false;
    return statusMeta[data.status]?.poll ?? false;
  }, [data]);

  async function loadOnce() {
    setError(null);
    const d = await apiFetch<DocumentDetails>(`/v1/organizations/${orgId}/documents/${docId}`);
    setData(d);
  }

  useEffect(() => {
    let active = true;
    (async () => {
      setLoading(true);
      try {
        const d = await apiFetch<DocumentDetails>(`/v1/organizations/${orgId}/documents/${docId}`);
        if (active) setData(d);
      } catch (e: any) {
        if (active) setError(e?.detail ?? "Не удалось загрузить документ");
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => {
      active = false;
    };
  }, [orgId, docId]);

  useEffect(() => {
    if (!shouldPoll) return;
    const t = setInterval(() => {
      loadOnce().catch(() => {});
    }, 3000);
    return () => clearInterval(t);
  }, [shouldPoll, orgId, docId]);

  if (loading) {
    return <p className="text-slate-300">Загрузка...</p>;
  }
  if (error) {
    return (
      <div className="space-y-4">
        <Card className="p-6">
          <p className="text-sm text-red-300">{error}</p>
          <div className="mt-4">
            <Link className="text-emerald-400 underline" href={`/organizations/${orgId}/documents`}>
              Назад
            </Link>
          </div>
        </Card>
      </div>
    );
  }
  if (!data) return null;

  return (
    <main className="space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div className="space-y-2">
          <h1 className="text-2xl font-semibold">{data.original_filename}</h1>
          <div className="flex flex-wrap items-center gap-3 text-sm text-slate-300">
            <span>тип: {data.type}</span>
            <StatusBadge status={data.status} />
            <span>страниц: {data.pages_count}</span>
            <span>{new Date(data.created_at).toLocaleString("ru-RU")}</span>
          </div>
        </div>
        <Link
          href={`/organizations/${orgId}/documents`}
          className="text-sm text-slate-300 underline hover:text-white"
        >
          К списку
        </Link>
      </div>

      {data.status === "failed" ? (
        <div className="rounded-2xl border border-red-800/40 bg-red-950/30 p-6 text-red-200">
          <div className="font-medium">Ошибка обработки</div>
          <div className="mt-2 text-sm opacity-90">{data.error_message ?? "Неизвестная ошибка"}</div>
        </div>
      ) : null}

      {data.pages?.length ? (
        <div className="space-y-4">
          <h2 className="text-lg font-medium text-white">OCR preview</h2>
          <div className="grid gap-4">
            {data.pages.map((p) => (
              <section key={p.page_number} className="rounded-2xl border border-slate-800 bg-slate-900/55 p-5">
                <div className="flex items-center justify-between">
                  <div className="text-sm text-slate-300">Страница {p.page_number}</div>
                  <div className="text-xs text-slate-400">confidence: {p.confidence.toFixed(2)}</div>
                </div>
                <pre className="mt-3 whitespace-pre-wrap text-sm text-slate-100">{p.ocr_text}</pre>
              </section>
            ))}
          </div>
        </div>
      ) : (
        <Card className="p-6 text-slate-300">
          OCR ещё не готов. Эта страница обновляется автоматически каждые 3 секунды, пока документ в статусе
          <span className="text-slate-100"> uploaded</span> или <span className="text-slate-100">queued</span>.
        </Card>
      )}
    </main>
  );
}

