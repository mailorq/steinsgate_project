import type { InputHTMLAttributes } from "react";

interface TextFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

export function TextField({ label, error, id, ...inputProps }: TextFieldProps) {
  return (
    <div className="w-full">
      <label
        className="mb-2 block text-xs font-medium tracking-widest text-zinc-400 uppercase"
        htmlFor={id}
      >
        {label}
      </label>
      <input
        id={id}
        className={`w-full rounded-lg border bg-zinc-900/80 px-4 py-3 text-sm text-zinc-100 placeholder-zinc-600 transition-colors focus:outline-none ${
          error
            ? "border-red-500/60 focus:border-red-500"
            : "border-zinc-800 hover:border-zinc-700 focus:border-amber-500/70"
        }`}
        {...inputProps}
      />
      {error && <div className="mt-1.5 text-xs text-red-400">{error}</div>}
    </div>
  );
}
