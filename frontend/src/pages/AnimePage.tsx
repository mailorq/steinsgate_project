import { useEffect } from "react";
import { Navigate, useParams } from "react-router-dom";

import { CommentsSection } from "@/features/comments/CommentsSection";
import { PlayerSwitcher } from "@/features/player/PlayerSwitcher";
import { RatingStars } from "@/features/rating/RatingStars";
import { findAnimeBySlug } from "@/shared/config/animes";
import type { AnimeInfo } from "@/shared/config/animes";
import { Faq } from "@/shared/ui/Faq";

export function AnimePage() {
  const { slug } = useParams();
  const anime = findAnimeBySlug(slug);

  useEffect(() => {
    if (anime) {
      document.title = anime.name;
    }
  }, [anime]);

  if (!anime) {
    return <Navigate to="/steins-gate" replace />;
  }

  return (
    <>
      <AnimeDescription anime={anime} />
      <PlayerSwitcher players={anime.players} />
      <Faq />
      <CommentsSection animeSlug={anime.slug} />
    </>
  );
}

function AnimeDescription({ anime }: { anime: AnimeInfo }) {
  return (
    <div className="mx-auto mt-4 mb-12 max-w-[80rem] px-3 md:mb-24 md:px-6">
      <div className="flex flex-col gap-4 rounded-xl bg-zinc-800/80 p-4 md:flex-row md:gap-6 md:p-6">
        <div className="flex aspect-[2/3] w-full flex-shrink-0 items-center justify-center overflow-hidden rounded-lg bg-zinc-700 md:w-[450px]">
          <img src={anime.poster} alt={anime.name} className="h-full w-full object-contain" />
        </div>

        <div className="flex flex-col overflow-hidden">
          <h2 className="mt-1 text-2xl font-bold md:text-4xl">{anime.name}</h2>
          <Divider />

          <div className="space-y-1 text-sm md:text-base">
            <div>
              <b>Сезон:</b> {anime.season}
            </div>
            <div>
              <b>Тип:</b> {anime.type}
            </div>
            <div>
              <b>Жанры:</b> {anime.genres}
            </div>
          </div>
          <Divider />

          <RatingStars animeSlug={anime.slug} />
          <Divider />

          <p className="line-clamp-[8] overflow-hidden text-sm leading-relaxed text-zinc-300 md:line-clamp-[10] md:text-lg">
            {anime.description}
          </p>
        </div>
      </div>
    </div>
  );
}

function Divider() {
  return <div className="my-3 h-px w-full bg-zinc-600/60 md:my-6" />;
}
