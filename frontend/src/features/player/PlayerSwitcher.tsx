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
    <div className="mx-auto w-full max-w-[1280px]">
      {players.length > 1 && (
        <div className="relative mb-2 w-full select-none">
          <div
            className="absolute top-0 left-0 h-full rounded-t-lg bg-red-600 transition-transform duration-300 ease-out"
            style={{
              width: `${100 / players.length}%`,
              transform: `translateX(${activeIndex * 100}%)`,
            }}
          />
          <div className="relative flex text-center text-sm font-medium md:text-lg">
            {players.map((player, index) => (
              <button
                key={player.label}
                type="button"
                onClick={() => setActiveIndex(index)}
                className="z-10 flex-1 py-2 md:py-3"
              >
                {player.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {players.map((player, index) => (
        <div key={player.src} className={index === activeIndex ? "block" : "hidden"}>
          <div className="relative w-full pb-[56.25%]">
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
