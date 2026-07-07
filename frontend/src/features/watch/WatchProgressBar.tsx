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
    <div className="mx-auto mb-2 w-full max-w-[1280px] px-3">
      <div className="flex items-center gap-3 text-sm text-zinc-400">
        <span>Прогресс просмотра:</span>
        <div className="h-2 flex-1 rounded-full bg-zinc-700">
          <div
            className="h-2 rounded-full bg-yellow-400"
            style={{ width: `${Math.min(progress.percentage, 100)}%` }}
          />
        </div>
        <span>{Math.round(progress.percentage)}%</span>
        <button
          type="button"
          onClick={onResume}
          className="rounded-lg bg-zinc-700 px-3 py-1 text-xs transition hover:bg-zinc-600 md:text-sm"
        >
          Продолжить с {formatTime(progress.current_time)}
        </button>
      </div>
    </div>
  );
}
