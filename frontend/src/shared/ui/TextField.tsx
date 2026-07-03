import type { InputHTMLAttributes } from "react";

interface TextFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

export function TextField({ label, error, id, ...inputProps }: TextFieldProps) {
  return (
    <div className="w-full">
      <label className="mb-2 block text-lg" htmlFor={id}>
        {label}
      </label>
      <input
        id={id}
        className="w-full rounded-lg bg-zinc-900/95 px-5 py-4 text-white focus:ring-2 focus:ring-yellow-400 focus:outline-none"
        {...inputProps}
      />
      {error && <div className="mt-1 text-sm text-red-500">{error}</div>}
    </div>
  );
}
