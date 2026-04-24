type Props = React.InputHTMLAttributes<HTMLInputElement> & {
  label: string;
  hint?: string;
};

export function Input({ label, hint, className, ...props }: Props) {
  return (
    <label className="block space-y-2">
      <span className="text-sm text-slate-300">{label}</span>
      <input
        className={`w-full rounded-xl border border-slate-800 bg-slate-950/60 px-3 py-2 text-slate-100 outline-none ring-0 placeholder:text-slate-600 focus:border-emerald-700/50 focus:outline-none ${
          className ?? ""
        }`}
        {...props}
      />
      {hint ? <div className="text-xs text-slate-500">{hint}</div> : null}
    </label>
  );
}

