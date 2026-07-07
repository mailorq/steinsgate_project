import { formatTime } from "./useWatchProgress";
import type { ProgressOut } from "@/shared/api";

interface WatchProgressBarProps {
  progress: ProgressOut | null;
  onResume: () => void;
}

export function WatchProgressBar({ progress, onResume }: WatchProgressBarProps) {
  if (!progress || progress.current_time < 10) {
    return null;
  }

  return (
    <div className="mx-auto mt-3 w-full max-w-5xl">
      <div className="flex items-center gap-3 rounded-xl border border-zinc-800/80 bg-zinc-950/60 px-4 py-2.5 text-xs text-zinc-500 md:text-sm">
        <span className="tracking-wide whitespace-nowrap uppercase">Прогресс</span>
        <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-zinc-800">
          <div
            className="h-1.5 rounded-full bg-amber-500 transition-all duration-500"
            style={{ width: `${Math.min(progress.percentage, 100)}%` }}
          />
        </div>
        <span className="font-mono text-zinc-400">{Math.round(progress.percentage)}%</span>
        <button
          type="button"
          onClick={onResume}
          className="rounded-lg border border-zinc-700 px-3 py-1 whitespace-nowrap text-zinc-300 transition-colors hover:border-amber-500/60 hover:text-amber-400"
        >
          Продолжить с {formatTime(progress.current_time)}
        </button>
      </div>
    </div>
  );
}
