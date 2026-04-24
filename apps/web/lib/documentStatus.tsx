export type DocumentStatus =
  | "pending_upload"
  | "uploaded"
  | "queued"
  | "ocr_done"
  | "parsed"
  | "analyzed"
  | "failed";

export const statusMeta: Record<
  DocumentStatus,
  { label: string; className: string; poll: boolean }
> = {
  pending_upload: {
    label: "ожидает загрузки",
    className: "bg-slate-700 text-slate-100",
    poll: false,
  },
  uploaded: {
    label: "загружен",
    className: "bg-blue-600/30 text-blue-200 border border-blue-700/40",
    poll: true,
  },
  queued: {
    label: "в очереди",
    className: "bg-amber-600/25 text-amber-200 border border-amber-700/40",
    poll: true,
  },
  ocr_done: {
    label: "OCR готов",
    className: "bg-emerald-600/25 text-emerald-200 border border-emerald-700/40",
    poll: false,
  },
  parsed: {
    label: "распознан",
    className: "bg-emerald-600/25 text-emerald-200 border border-emerald-700/40",
    poll: false,
  },
  analyzed: {
    label: "проанализирован",
    className: "bg-emerald-600/25 text-emerald-200 border border-emerald-700/40",
    poll: false,
  },
  failed: {
    label: "ошибка",
    className: "bg-red-600/25 text-red-200 border border-red-700/40",
    poll: false,
  },
};

export function StatusBadge({ status }: { status: DocumentStatus }) {
  const meta = statusMeta[status] ?? statusMeta.failed;
  return (
    <span className={`inline-flex items-center rounded-full px-2 py-1 text-xs ${meta.className}`}>
      {meta.label}
    </span>
  );
}

