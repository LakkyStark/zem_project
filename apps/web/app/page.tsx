const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function HomePage() {
  return (
    <main className="mx-auto flex max-w-3xl flex-col gap-10 px-6 py-16">
      <header className="space-y-3">
        <p className="text-sm uppercase tracking-wide text-emerald-400/90">MVP scaffold</p>
        <h1 className="text-4xl font-semibold tracking-tight text-white">BuildLaw AI</h1>
        <p className="text-lg text-slate-300">
          Монорепозиторий: Next.js 15, FastAPI, воркер Redis, PostgreSQL и S3-совместимое
          хранилище (MinIO).
        </p>
      </header>
      <section className="rounded-xl border border-slate-800 bg-slate-900/60 p-6 shadow-lg shadow-emerald-900/10">
        <h2 className="text-lg font-medium text-white">Локальная разработка</h2>
        <ul className="mt-4 list-disc space-y-2 pl-5 text-slate-300">
          <li>
            API и OpenAPI:{" "}
            <a className="text-emerald-400 underline" href={`${apiUrl}/docs`}>
              {apiUrl}/docs
            </a>
          </li>
          <li>Подробные шаги — в корневом README.md репозитория.</li>
        </ul>
      </section>
    </main>
  );
}
