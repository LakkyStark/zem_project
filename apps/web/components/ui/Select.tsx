type Props = React.SelectHTMLAttributes<HTMLSelectElement> & {
  label: string;
};

export function Select({ label, className, children, ...props }: Props) {
  return (
    <label className="grid gap-2">
      <span className="text-sm text-slate-300">{label}</span>
      <select
        className={`rounded-xl border border-slate-800 bg-slate-950/60 px-3 py-2 text-slate-100 outline-none focus:border-emerald-700/50 ${
          className ?? ""
        }`}
        {...props}
      >
        {children}
      </select>
    </label>
  );
}

