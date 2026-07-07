import type { ReactNode } from "react";

interface FormCardProps {
  title: string;
  subtitle?: string;
  maxWidthClass?: string;
  children: ReactNode;
}

export function FormCard({
  title,
  subtitle,
  maxWidthClass = "max-w-[50rem]",
  children,
}: FormCardProps) {
  return (
    <div className={`${maxWidthClass} mx-auto mt-8 mb-12 rounded-xl bg-zinc-800/80 p-8 shadow-lg`}>
      <h2 className="mb-6 text-center text-3xl font-bold md:text-4xl">{title}</h2>
      {subtitle && <h3 className="mb-3 text-center text-xl italic text-zinc-300 md:text-2xl">{subtitle}</h3>}
      {children}
    </div>
  );
}
