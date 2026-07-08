import { useState } from "react";
import type { FormEvent } from "react";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { ApiError, commentsApi } from "@/shared/api";
import type { CommentOut, CommentPageOut } from "@/shared/api";
import { useSession } from "@/shared/session/SessionContext";
import { Avatar } from "@/shared/ui/Avatar";

const COMMENTS_OPEN_KEY = "comments_open";

interface CommentsSectionProps {
  animeSlug: string;
}

export function CommentsSection({ animeSlug }: CommentsSectionProps) {
  const { user } = useSession();
  const queryClient = useQueryClient();
  const [text, setText] = useState("");
  const [page, setPage] = useState(1);
  const [error, setError] = useState<string | null>(null);
  const [isOpen, setIsOpen] = useState(() => localStorage.getItem(COMMENTS_OPEN_KEY) === "1");

  const queryKey = ["comments", animeSlug, page];
  const { data } = useQuery({
    queryKey,
    queryFn: () => commentsApi.list(animeSlug, page),
    placeholderData: (previous) => previous,
  });

  const createMutation = useMutation({
    mutationFn: (commentText: string) => commentsApi.create(animeSlug, commentText),
    onSuccess: () => {
      setText("");
      setError(null);
      setPage(1);
      queryClient.invalidateQueries({ queryKey: ["comments", animeSlug] });
    },
    onError: (requestError) => {
      setError(
        requestError instanceof ApiError ? requestError.message : "Не удалось отправить комментарий",
      );
    },
  });

  const reactMutation = useMutation({
    mutationFn: ({ commentId, isLike }: { commentId: number; isLike: boolean }) =>
      commentsApi.react(commentId, isLike),
    onSuccess: (result, { commentId, isLike }) => {
      queryClient.setQueryData<CommentPageOut>(queryKey, (old) => {
        if (!old) {
          return old;
        }
        return {
          ...old,
          items: old.items.map((comment) => {
            if (comment.id !== commentId) {
              return comment;
            }
            const reaction = isLike ? "like" : "dislike";
            return {
              ...comment,
              likes: result.likes,
              dislikes: result.dislikes,
              my_reaction: comment.my_reaction === reaction ? null : reaction,
            };
          }),
        };
      });
    },
  });

  const comments = data?.items ?? [];
  const totalPages = data?.total_pages ?? 1;

  function toggleOpen() {
    setIsOpen((open) => {
      localStorage.setItem(COMMENTS_OPEN_KEY, open ? "0" : "1");
      return !open;
    });
  }

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const trimmed = text.trim();
    if (!user || trimmed.length < 3 || trimmed.length > 2000) {
      return;
    }
    createMutation.mutate(trimmed);
  }

  return (
    <div className="mx-auto mt-10 mb-16 max-w-4xl px-3 md:mt-14 md:mb-24 md:px-0">
      <div className="rounded-2xl border border-zinc-800/80 bg-zinc-950/60 p-5 backdrop-blur-sm md:p-7">
        <button
          type="button"
          onClick={toggleOpen}
          className="flex w-full items-center justify-between text-left text-lg font-semibold tracking-tight md:text-xl"
        >
          <span>Комментарии</span>
          <span
            className={`text-base text-amber-500 transition-transform duration-300 md:text-lg ${isOpen ? "rotate-180" : ""}`}
          >
            ˅
          </span>
        </button>

        <div
          className={`grid transition-all duration-300 ease-out ${isOpen ? "grid-rows-[1fr]" : "grid-rows-[0fr]"}`}
        >
          <div className="overflow-hidden">
            <div className="mt-4 md:mt-6">
              {user ? (
                <form onSubmit={handleSubmit} className="mb-6 md:mb-10">
                  <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    rows={3}
                    placeholder="Написать комментарий..."
                    required
                    className="w-full resize-none rounded-lg border border-zinc-800 bg-zinc-900/80 p-3 text-sm text-zinc-100 placeholder-zinc-600 transition-colors hover:border-zinc-700 focus:border-amber-500/70 focus:outline-none md:p-4"
                  />
                  {error && <div className="mt-2 text-sm text-red-500">{error}</div>}
                  <button
                    type="submit"
                    disabled={createMutation.isPending}
                    className="mt-3 inline-flex items-center justify-center rounded-lg bg-amber-500 px-5 py-2.5 text-sm font-semibold text-zinc-950 transition-all duration-200 hover:bg-amber-400 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-40 md:mt-4"
                  >
                    Отправить
                  </button>
                </form>
              ) : (
                <div className="mb-6 rounded-xl border border-zinc-800 bg-zinc-900/50 p-4 text-center text-sm text-zinc-500 md:mb-8">
                  Чтобы оставить комментарий войдите в аккаунт
                </div>
              )}

              <div className="space-y-4 md:space-y-6">
                {comments.length === 0 ? (
                  <div className="text-center text-zinc-500">Пока нет комментариев</div>
                ) : (
                  comments.map((comment) => (
                    <CommentCard
                      key={comment.id}
                      comment={comment}
                      canReact={user !== null}
                      onReact={(commentId, isLike) => reactMutation.mutate({ commentId, isLike })}
                    />
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {totalPages > 1 && (
        <div className="mt-6 flex flex-wrap items-center justify-center gap-2 md:mt-10 md:gap-4">
          {page > 1 && (
            <button
              type="button"
              onClick={() => setPage(page - 1)}
              className="rounded-lg border border-zinc-700 px-4 py-2 text-sm text-zinc-300 transition-colors hover:border-zinc-500 hover:text-zinc-100"
            >
              ← Назад
            </button>
          )}
          <span className="text-sm text-zinc-400 md:text-base">
            Страница {page} из {totalPages}
          </span>
          {page < totalPages && (
            <button
              type="button"
              onClick={() => setPage(page + 1)}
              className="rounded-lg border border-zinc-700 px-4 py-2 text-sm text-zinc-300 transition-colors hover:border-zinc-500 hover:text-zinc-100"
            >
              Далее →
            </button>
          )}
        </div>
      )}
    </div>
  );
}

function CommentCard({
  comment,
  canReact,
  onReact,
}: {
  comment: CommentOut;
  canReact: boolean;
  onReact: (commentId: number, isLike: boolean) => void;
}) {
  return (
    <div className="rounded-xl border border-zinc-800/70 bg-zinc-900/50 p-4 transition-all duration-200 hover:border-zinc-700 hover:bg-zinc-900/80 md:p-5">
      <div className="mb-3 flex items-start justify-between gap-3">
        <div className="flex min-w-0 flex-1 items-center gap-3">
          <Avatar
            avatarUrl={comment.author.avatar_url}
            username={comment.author.username}
            sizeClass="w-10 h-10 md:w-12 md:h-12"
            textSizeClass="text-base md:text-lg"
          />
          <div className="min-w-0 flex-1">
            <div className="truncate text-sm font-semibold text-amber-400/90 md:text-base">
              {comment.author.nickname || comment.author.username}
            </div>
          </div>
        </div>
        <span className="flex-shrink-0 text-xs whitespace-nowrap text-zinc-500 md:text-sm">
          {formatDate(new Date(comment.created_at))}
        </span>
      </div>

      <p className="overflow-hidden text-sm leading-relaxed break-words hyphens-auto whitespace-pre-line text-zinc-300 md:text-base">
        {comment.text}
      </p>

      {canReact && (
        <div className="mt-3 flex items-center gap-4">
          <button
            type="button"
            onClick={() => onReact(comment.id, true)}
            className={`flex items-center gap-1 text-xs transition md:text-sm ${
              comment.my_reaction === "like" ? "text-emerald-400" : "text-zinc-500 hover:text-emerald-400"
            }`}
          >
            <ThumbIcon up />
            <span>{comment.likes}</span>
          </button>
          <button
            type="button"
            onClick={() => onReact(comment.id, false)}
            className={`flex items-center gap-1 text-xs transition md:text-sm ${
              comment.my_reaction === "dislike" ? "text-red-400" : "text-zinc-500 hover:text-red-400"
            }`}
          >
            <ThumbIcon />
            <span>{comment.dislikes}</span>
          </button>
          <span className="text-xs text-zinc-500 md:text-sm">
            Рейтинг: <span>{comment.likes - comment.dislikes}</span>
          </span>
        </div>
      )}
    </div>
  );
}

function ThumbIcon({ up = false }: { up?: boolean }) {
  return (
    <svg
      className={`h-4 w-4 ${up ? "" : "rotate-180"}`}
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="2"
        d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5"
      />
    </svg>
  );
}

function formatDate(date: Date): string {
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${pad(date.getDate())}.${pad(date.getMonth() + 1)}.${date.getFullYear()} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
}
