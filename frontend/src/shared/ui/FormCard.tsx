import type { ReactNode } from "react";

interface FormCardProps {
  title: string;
  subtitle?: string;
  maxWidthClass?: string;
  children: ReactNode;
}

export function FormCard({ title, subtitle, maxWidthClass = "max-w-md", children }: FormCardProps) {
  return (
    <div
      className={`${maxWidthClass} mx-auto mt-10 mb-16 rounded-2xl border border-zinc-800/80 bg-zinc-950/60 p-8 shadow-2xl shadow-black/40 backdrop-blur-sm md:p-10`}
    >
      <h2 className="text-center text-2xl font-semibold tracking-tight text-zinc-100">{title}</h2>
      {subtitle && <p className="mt-3 text-center text-sm leading-relaxed text-zinc-500">{subtitle}</p>}
      <div className="mt-8">{children}</div>
    </div>
  );
}
