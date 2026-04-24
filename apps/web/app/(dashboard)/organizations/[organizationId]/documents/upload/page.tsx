"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useMemo, useState } from "react";

import { apiFetch } from "@/lib/api";

type UploadSessionRequest = {
  type: string;
  original_filename: string;
  mime_type: string;
  size_bytes?: number | null;
};

type UploadSessionResponse = {
  document_id: string;
  storage_key: string;
  status: string;
  upload_url: string;
  upload_method: "PUT";
  expires_in_seconds: number;
};

type CompleteResponse = { document_id: string; status: string; queued: boolean };

type Step = "idle" | "preparing" | "uploading" | "finalizing" | "queued" | "error";

export default function UploadPage() {
  const params = useParams<{ organizationId: string }>();
  const orgId = params.organizationId;
  const router = useRouter();

  const [file, setFile] = useState<File | null>(null);
  const [docType, setDocType] = useState<"egrn" | "authority_refusal" | "other">("egrn");
  const [step, setStep] = useState<Step>("idle");
  const [error, setError] = useState<string | null>(null);

  const canSubmit = useMemo(() => !!file && step !== "uploading" && step !== "finalizing", [file, step]);

  async function startUpload() {
    if (!file) return;
    setError(null);
    setStep("preparing");
    try {
      const body: UploadSessionRequest = {
        type: docType,
        original_filename: file.name,
        mime_type: file.type || "application/octet-stream",
        size_bytes: file.size,
      };
      const session = await apiFetch<UploadSessionResponse>(
        `/v1/organizations/${orgId}/documents/upload-sessions`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        }
      );

      setStep("uploading");
      const put = await fetch(session.upload_url, {
        method: "PUT",
        headers: { "Content-Type": body.mime_type },
        body: file,
      });
      if (!put.ok) {
        throw new Error("Не удалось загрузить файл в хранилище");
      }

      setStep("finalizing");
      const complete = await apiFetch<CompleteResponse>(
        `/v1/organizations/${orgId}/documents/${session.document_id}/complete-upload`,
        { method: "POST" }
      );
      setStep("queued");
      router.push(`/organizations/${orgId}/documents/${complete.document_id}`);
    } catch (e: any) {
      setError(e?.detail ?? e?.message ?? "Ошибка загрузки");
      setStep("error");
    }
  }

  return (
    <main className="space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">Загрузка документа</h1>
          <p className="text-slate-300">Создаём upload session → PUT в S3/MinIO → complete-upload.</p>
        </div>
        <Link
          href={`/organizations/${orgId}/documents`}
          className="text-sm text-slate-300 underline hover:text-white"
        >
          Назад к списку
        </Link>
      </div>

      <div
        className="rounded-xl border border-dashed border-slate-700 bg-slate-900/40 p-8"
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          const f = e.dataTransfer.files?.[0];
          if (f) setFile(f);
        }}
      >
        <div className="space-y-3">
          <div className="text-sm text-slate-300">Перетащите файл сюда или выберите через picker</div>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            className="block w-full text-sm text-slate-300 file:mr-4 file:rounded-lg file:border-0 file:bg-slate-800 file:px-4 file:py-2 file:text-slate-100 hover:file:bg-slate-700"
          />
          {file ? (
            <div className="text-sm text-slate-200">
              Выбран: <span className="font-medium">{file.name}</span> ({Math.ceil(file.size / 1024)} KB)
            </div>
          ) : null}
        </div>
      </div>

      <div className="grid gap-4 rounded-xl border border-slate-800 bg-slate-900/60 p-6">
        <label className="grid gap-2">
          <span className="text-sm text-slate-300">Тип документа</span>
          <select
            value={docType}
            onChange={(e) => setDocType(e.target.value as any)}
            className="rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 text-slate-100"
          >
            <option value="egrn">egrn</option>
            <option value="authority_refusal">authority_refusal</option>
            <option value="other">other</option>
          </select>
        </label>

        {error ? <p className="text-sm text-red-300">{error}</p> : null}

        <div className="flex items-center justify-between gap-4">
          <div className="text-sm text-slate-400">
            Статус:{" "}
            <span className="text-slate-200">
              {step === "idle"
                ? "готово"
                : step === "preparing"
                ? "preparing"
                : step === "uploading"
                ? "uploading"
                : step === "finalizing"
                ? "finalizing"
                : step === "queued"
                ? "queued"
                : "error"}
            </span>
          </div>
          <button
            onClick={startUpload}
            disabled={!canSubmit}
            className="rounded-lg bg-emerald-500 px-4 py-2 font-medium text-slate-950 disabled:opacity-60"
          >
            Загрузить
          </button>
        </div>
      </div>
    </main>
  );
}

