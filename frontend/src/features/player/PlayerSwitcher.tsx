import { useState } from "react";

import type { AnimePlayer } from "@/shared/config/animes";

interface PlayerSwitcherProps {
  players: AnimePlayer[];
}

export function PlayerSwitcher({ players }: PlayerSwitcherProps) {
  const [activeIndex, setActiveIndex] = useState(0);

  if (players.length === 0) {
    return null;
  }

  return (
    <div className="mx-auto w-full max-w-5xl">
      {players.length > 1 && (
        <div className="relative mb-3 flex w-full select-none rounded-xl border border-zinc-800 bg-zinc-950/70 p-1">
          <div
            className="absolute top-1 bottom-1 rounded-lg bg-zinc-800 transition-transform duration-300 ease-out"
            style={{
              width: `calc(${100 / players.length}% - 4px)`,
              transform: `translateX(calc(${activeIndex * 100}% + ${activeIndex * 4}px))`,
              left: "4px",
            }}
          />
          {players.map((player, index) => (
            <button
              key={player.label}
              type="button"
              onClick={() => setActiveIndex(index)}
              className={`z-10 flex-1 rounded-lg py-2 text-sm font-medium transition-colors duration-200 ${
                index === activeIndex ? "text-amber-400" : "text-zinc-500 hover:text-zinc-300"
              }`}
            >
              {player.label}
            </button>
          ))}
        </div>
      )}

      {players.map((player, index) => (
        <div key={player.src} className={index === activeIndex ? "block" : "hidden"}>
          <div className="relative w-full overflow-hidden rounded-2xl border border-zinc-800/80 pb-[56.25%] shadow-2xl shadow-black/40">
            <iframe
              src={player.src}
              title={player.label}
              allowFullScreen
              className="player-embed absolute top-0 left-0 h-full w-full"
            />
          </div>
        </div>
      ))}
    </div>
  );
}
