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
    <header className="fixed top-0 right-0 left-0 z-50 flex items-center justify-between bg-zinc-900 px-4 py-3 text-white md:px-9 md:py-4">
      <DivergenceMeter value={worldline} />

      <div className="group relative ml-2 md:ml-6">
        <button
          type="button"
          className="flex cursor-pointer items-center gap-1 text-xs transition-colors hover:text-orange-400 md:gap-2 md:text-sm"
        >
          <span className="font-mono text-sm tracking-wide uppercase md:text-base md:tracking-widest">
            Линии
          </span>
          <svg
            className="h-2.5 w-2.5 opacity-60 md:h-3 md:w-3"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>

        <ul className="invisible absolute left-0 mt-2 w-48 rounded-lg border border-zinc-700 bg-zinc-900 opacity-0 shadow-xl transition-all duration-200 group-hover:visible group-hover:opacity-100 md:w-56">
          {ANIMES.map((anime) => (
            <li key={anime.slug}>
              <Link
                to={`/${anime.slug}`}
                className="flex justify-between px-3 py-2 transition-colors hover:bg-zinc-800 md:px-4 md:py-2.5"
              >
                <span className="font-mono text-xs text-orange-500 md:text-sm">
                  {anime.worldline}
                </span>
                <span className="text-xs text-zinc-400 md:text-sm">{anime.menuLabel}</span>
              </Link>
            </li>
          ))}
        </ul>
      </div>

      <Link
        to="/future-gadget-laboratory"
        className="absolute left-1/2 hidden -translate-x-1/2 cursor-pointer text-2xl font-bold transition-colors hover:text-gray-200 md:block lg:text-4xl"
      >
        Future Gadget Laboratory
      </Link>

      <Link
        to={user ? "/profile" : "/register"}
        className="ml-auto transition-transform hover:scale-105"
      >
        <img
          src="/img/register_bin.webp"
          alt={user ? "Профиль" : "Регистрация"}
          className="h-12 w-auto transition duration-200 hover:scale-110 md:h-20"
        />
      </Link>
    </header>
  );
}
