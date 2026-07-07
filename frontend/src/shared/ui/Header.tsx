import { Link, useLocation } from "react-router-dom";

import { ANIMES, findAnimeBySlug } from "@/shared/config/animes";
import { useSession } from "@/shared/session/SessionContext";
import { DivergenceMeter } from "@/shared/ui/DivergenceMeter";

const DEFAULT_WORLDLINE = "0.000000";

export function Header() {
  const { pathname } = useLocation();
  const { user } = useSession();
  const currentAnime = findAnimeBySlug(pathname.replace(/^\/|\/$/g, ""));
  const worldline = currentAnime?.worldline ?? DEFAULT_WORLDLINE;

  return (
    <header className="fixed top-0 right-0 left-0 z-50 border-b border-zinc-800/70 bg-zinc-950/80 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-3 px-3 py-2.5 md:px-6 md:py-3">
        <div className="flex items-center gap-1 md:gap-2">
          <DivergenceMeter value={worldline} />

          <div className="group relative">
          <button
            type="button"
            className="flex cursor-pointer items-center gap-1.5 rounded-lg px-2 py-1.5 text-zinc-400 transition-colors hover:text-amber-400 md:px-3"
          >
            <span className="font-mono text-xs tracking-widest uppercase md:text-sm">Линии</span>
            <svg
              className="h-2.5 w-2.5 opacity-60 transition-transform duration-200 group-hover:rotate-180 md:h-3 md:w-3"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          <ul className="invisible absolute left-0 mt-2 w-52 overflow-hidden rounded-xl border border-zinc-800 bg-zinc-950/95 opacity-0 shadow-2xl shadow-black/50 backdrop-blur-md transition-all duration-200 group-hover:visible group-hover:opacity-100 md:w-60">
            {ANIMES.map((anime) => (
              <li key={anime.slug}>
                <Link
                  to={`/${anime.slug}`}
                  className={`flex items-center justify-between px-4 py-2.5 transition-colors hover:bg-zinc-900 ${
                    currentAnime?.slug === anime.slug ? "bg-zinc-900/60" : ""
                  }`}
                >
                  <span className="font-mono text-xs text-amber-500 md:text-sm">
                    {anime.worldline}
                  </span>
                  <span className="text-xs text-zinc-400 md:text-sm">{anime.menuLabel}</span>
                </Link>
              </li>
            ))}
          </ul>
          </div>
        </div>

        <Link
          to="/future-gadget-laboratory"
          className="absolute left-1/2 hidden -translate-x-1/2 text-sm font-semibold tracking-[0.25em] text-zinc-200 uppercase transition-colors hover:text-amber-400 md:block lg:text-base"
        >
          Future Gadget Laboratory
        </Link>

        <Link
          to={user ? "/profile" : "/register"}
          className="rounded-lg px-2 py-1 transition-transform hover:scale-105 md:px-3"
        >
          <img
            src="/img/register_bin.webp"
            alt={user ? "Профиль" : "Регистрация"}
            className="h-11 w-auto md:h-12"
          />
        </Link>
      </div>
    </header>
  );
}
