export default function HomePage() {
  return (
    <div className="bg-grid">
      <main className="mx-auto flex max-w-6xl flex-col gap-16 px-6 py-14">
        <header className="flex flex-col gap-8">
          <div className="flex items-center justify-between gap-4">
            <div className="text-sm font-medium tracking-wide text-emerald-300/90">
              AI SaaS • документы строительства и земли
            </div>
            <div className="flex items-center gap-2">
              <a
                className="rounded-xl border border-slate-800 bg-slate-900/40 px-3 py-2 text-sm text-slate-200 hover:bg-slate-900/60"
                href="/login"
              >
                Войти
              </a>
              <a
                className="rounded-xl bg-emerald-500 px-3 py-2 text-sm font-medium text-slate-950 hover:bg-emerald-400"
                href="/register"
              >
                Попробовать бесплатно
              </a>
            </div>
          </div>

          <div className="max-w-3xl space-y-4">
            <h1 className="text-5xl font-semibold tracking-tight text-white">
              BuildLaw AI — анализ документов в 3 шага
            </h1>
            <p className="text-lg text-slate-300">
              Загрузка PDF → Mock OCR → предпросмотр страниц → дальше: парсинг, извлечение сущностей,
              проверка рисков и отчёты по шаблонам.
            </p>
            <div className="flex flex-wrap items-center gap-3 pt-2">
              <a
                className="rounded-xl bg-emerald-500 px-4 py-2 text-sm font-medium text-slate-950 hover:bg-emerald-400"
                href="/register"
              >
                Начать
              </a>
              <a
                className="rounded-xl border border-slate-800 bg-slate-900/40 px-4 py-2 text-sm text-slate-200 hover:bg-slate-900/60"
                href="/organizations"
              >
                Перейти в кабинет
              </a>
            </div>
          </div>
        </header>

        <section className="grid gap-4 md:grid-cols-3">
          <div className="rounded-2xl border border-slate-800 bg-slate-900/55 p-6">
            <div className="text-xs font-semibold text-slate-400">01</div>
            <div className="mt-2 text-lg font-medium text-white">Загрузите документ</div>
            <div className="mt-2 text-sm text-slate-300">
              Обычный PDF: ЕГРН, отказ органа, договор, приложение.
            </div>
          </div>
          <div className="rounded-2xl border border-slate-800 bg-slate-900/55 p-6">
            <div className="text-xs font-semibold text-slate-400">02</div>
            <div className="mt-2 text-lg font-medium text-white">OCR и статус</div>
            <div className="mt-2 text-sm text-slate-300">
              Очередь → обработка → OCR preview по страницам, без ручных действий.
            </div>
          </div>
          <div className="rounded-2xl border border-slate-800 bg-slate-900/55 p-6">
            <div className="text-xs font-semibold text-slate-400">03</div>
            <div className="mt-2 text-lg font-medium text-white">Следующие модули</div>
            <div className="mt-2 text-sm text-slate-300">
              Парсинг, извлечение атрибутов, анализ рисков, биллинг и роли.
            </div>
          </div>
        </section>

        <section className="rounded-2xl border border-slate-800 bg-slate-900/55 p-8">
          <div className="grid gap-8 md:grid-cols-2">
            <div className="space-y-3">
              <h2 className="text-2xl font-semibold tracking-tight text-white">Сквозной MVP уже работает</h2>
              <p className="text-slate-300">
                Регистрация → организация → загрузка → очередь → OCR → предпросмотр. Это база для дальнейшего
                продакшн‑конвейера.
              </p>
              <div className="flex flex-wrap gap-2 text-xs text-slate-300">
                <span className="rounded-full border border-slate-800 bg-slate-950/40 px-3 py-1">
                  Next.js 15
                </span>
                <span className="rounded-full border border-slate-800 bg-slate-950/40 px-3 py-1">
                  FastAPI
                </span>
                <span className="rounded-full border border-slate-800 bg-slate-950/40 px-3 py-1">
                  Postgres
                </span>
                <span className="rounded-full border border-slate-800 bg-slate-950/40 px-3 py-1">
                  Redis + RQ
                </span>
                <span className="rounded-full border border-slate-800 bg-slate-950/40 px-3 py-1">
                  S3-compatible
                </span>
              </div>
            </div>
            <div className="space-y-3">
              <div className="text-sm font-medium text-slate-200">Пример статусов</div>
              <div className="grid gap-3 sm:grid-cols-2">
                {[
                  ["uploaded", "Файл загружен"],
                  ["queued", "В очереди"],
                  ["ocr_done", "OCR готов"],
                  ["failed", "Ошибка"],
                ].map(([k, v]) => (
                  <div key={k} className="rounded-xl border border-slate-800 bg-slate-950/30 p-4">
                    <div className="text-xs text-slate-400">{k}</div>
                    <div className="mt-1 text-sm text-slate-200">{v}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <footer className="flex flex-col items-start justify-between gap-3 border-t border-slate-900/80 py-8 text-sm text-slate-400 md:flex-row md:items-center">
          <div>© {new Date().getFullYear()} BuildLaw AI</div>
          <div className="flex items-center gap-4">
            <a className="hover:text-slate-200" href="/login">
              Вход
            </a>
            <a className="hover:text-slate-200" href="/register">
              Регистрация
            </a>
          </div>
        </footer>
      </main>
    </div>
  );
}
