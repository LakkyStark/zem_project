import Link from "next/link";

type Props = {
  href?: string;
  children: React.ReactNode;
  variant?: "primary" | "secondary" | "ghost";
  className?: string;
  type?: "button" | "submit";
  disabled?: boolean;
  onClick?: () => void;
};

const variants: Record<NonNullable<Props["variant"]>, string> = {
  primary:
    "bg-emerald-500 text-slate-950 hover:bg-emerald-400 shadow-[0_0_0_1px_rgba(16,185,129,.25),0_10px_30px_rgba(16,185,129,.12)]",
  secondary: "bg-slate-900/70 text-slate-100 hover:bg-slate-900 border border-slate-800",
  ghost: "bg-transparent text-slate-200 hover:bg-slate-900/40 border border-slate-800/60",
};

export function Button({
  href,
  children,
  variant = "primary",
  className,
  type = "button",
  disabled,
  onClick,
}: Props) {
  const cls = `inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2 text-sm font-medium transition disabled:opacity-60 ${variants[variant]} ${
    className ?? ""
  }`;

  if (href) {
    return (
      <Link className={cls} href={href}>
        {children}
      </Link>
    );
  }

  return (
    <button className={cls} type={type} disabled={disabled} onClick={onClick}>
      {children}
    </button>
  );
}

