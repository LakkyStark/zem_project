export function Card({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={`rounded-2xl border border-slate-800 bg-slate-900/55 shadow-[0_1px_0_0_rgba(255,255,255,.03),0_20px_80px_rgba(0,0,0,.35)] ${
        className ?? ""
      }`}
    >
      {children}
    </div>
  );
}

