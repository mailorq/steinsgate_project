import { useState } from "react";
import type { FormEvent } from "react";

import { useSession } from "@/shared/session/SessionContext";
import { Avatar } from "@/shared/ui/Avatar";

const COMMENTS_PER_PAGE = 6;
const COMMENTS_OPEN_KEY = "comments_open";

export interface CommentData {
  id: number;
  author: {
    username: string;
    nickname: string;
    avatarUrl: string | null;
  };
  text: string;
  createdAt: Date;
  likes: number;
  dislikes: number;
  myReaction: "like" | "dislike" | null;
}

interface CommentsSectionProps {
  animeSlug: string;
}

export function CommentsSection({ animeSlug }: CommentsSectionProps) {
  const { user } = useSession();
  const [comments, setComments] = useState<CommentData[]>([]);
  const [text, setText] = useState("");
  const [page, setPage] = useState(1);
  const [isOpen, setIsOpen] = useState(() => localStorage.getItem(COMMENTS_OPEN_KEY) === "1");

  void animeSlug;

  const totalPages = Math.max(1, Math.ceil(comments.length / COMMENTS_PER_PAGE));
  const pageComments = comments.slice((page - 1) * COMMENTS_PER_PAGE, page * COMMENTS_PER_PAGE);

  function toggleOpen() {
    setIsOpen((open) => {
      localStorage.setItem(COMMENTS_OPEN_KEY, open ? "0" : "1");
      return !open;
    });
  }

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const trimmed = text.trim();
    if (!user || trimmed.length < 3 || trimmed.length >= 2000) {
      return;
    }
    const newComment: CommentData = {
      id: Date.now(),
      author: { username: user.username, nickname: user.nickname, avatarUrl: user.avatarUrl },
      text: trimmed,
      createdAt: new Date(),
      likes: 0,
      dislikes: 0,
      myReaction: null,
    };
    setComments((current) => [newComment, ...current]);
    setText("");
    setPage(1);
  }

  function react(commentId: number, reaction: "like" | "dislike") {
    setComments((current) =>
      current.map((comment) => {
        if (comment.id !== commentId) {
          return comment;
        }
        const next = { ...comment };
        if (next.myReaction === reaction) {
          next.myReaction = null;
          next[reaction === "like" ? "likes" : "dislikes"] -= 1;
        } else {
          if (next.myReaction) {
            next[next.myReaction === "like" ? "likes" : "dislikes"] -= 1;
          }
          next.myReaction = reaction;
          next[reaction === "like" ? "likes" : "dislikes"] += 1;
        }
        return next;
      }),
    );
  }

  return (
    <div className="mx-auto mt-12 mb-16 max-w-[80rem] px-3 md:mt-24 md:mb-32 md:px-6">
      <div className="rounded-xl bg-zinc-800/80 p-4 md:p-8">
        <button
          type="button"
          onClick={toggleOpen}
          className="flex w-full items-center justify-between text-left text-xl font-bold md:text-3xl"
        >
          <span>Комментарии</span>
          <span
            className={`text-lg text-red-500 transition-transform duration-300 md:text-2xl ${isOpen ? "rotate-180" : ""}`}
          >
            ˅
          </span>
        </button>

        <div
          className={`grid transition-all duration-500 ease-in-out ${isOpen ? "grid-rows-[1fr]" : "grid-rows-[0fr]"}`}
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
                    className="w-full resize-none rounded-lg bg-zinc-900 p-3 text-sm text-white focus:ring-2 focus:ring-red-500 focus:outline-none md:p-4 md:text-base"
                  />
                  <button
                    type="submit"
                    className="mt-3 rounded-lg bg-red-600 px-4 py-2 text-sm font-medium transition hover:bg-red-700 md:mt-4 md:px-6 md:text-base"
                  >
                    Отправить
                  </button>
                </form>
              ) : (
                <div className="mb-6 rounded-lg bg-zinc-900 p-3 text-center text-sm text-zinc-400 md:mb-8 md:p-4 md:text-base">
                  Чтобы оставить комментарий войдите в аккаунт
                </div>
              )}

              <div className="space-y-4 md:space-y-6">
                {pageComments.length === 0 ? (
                  <div className="text-center text-zinc-500">Пока нет комментариев</div>
                ) : (
                  pageComments.map((comment) => (
                    <CommentCard
                      key={comment.id}
                      comment={comment}
                      canReact={user !== null}
                      onReact={react}
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
              className="rounded-lg bg-zinc-700 px-3 py-2 text-sm transition hover:bg-zinc-600 md:px-4 md:text-base"
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
              className="rounded-lg bg-zinc-700 px-3 py-2 text-sm transition hover:bg-zinc-600 md:px-4 md:text-base"
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
  comment: CommentData;
  canReact: boolean;
  onReact: (commentId: number, reaction: "like" | "dislike") => void;
}) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4 transition-colors hover:border-zinc-700 md:p-6">
      <div className="mb-3 flex items-start justify-between gap-3">
        <div className="flex min-w-0 flex-1 items-center gap-3">
          <Avatar
            avatarUrl={comment.author.avatarUrl}
            username={comment.author.username}
            sizeClass="w-10 h-10 md:w-12 md:h-12"
            textSizeClass="text-base md:text-lg"
          />
          <div className="min-w-0 flex-1">
            <div className="truncate text-base font-bold text-red-500 md:text-lg">
              {comment.author.nickname || comment.author.username}
            </div>
          </div>
        </div>
        <span className="flex-shrink-0 text-xs whitespace-nowrap text-zinc-500 md:text-sm">
          {formatDate(comment.createdAt)}
        </span>
      </div>

      <p className="overflow-hidden text-sm leading-relaxed break-words hyphens-auto whitespace-pre-line text-zinc-300 md:text-base">
        {comment.text}
      </p>

      {canReact && (
        <div className="mt-3 flex items-center gap-4">
          <button
            type="button"
            onClick={() => onReact(comment.id, "like")}
            className={`flex items-center gap-1 text-xs transition md:text-sm ${
              comment.myReaction === "like" ? "text-green-400" : "text-zinc-400 hover:text-green-400"
            }`}
          >
            <ThumbIcon up />
            <span>{comment.likes}</span>
          </button>
          <button
            type="button"
            onClick={() => onReact(comment.id, "dislike")}
            className={`flex items-center gap-1 text-xs transition md:text-sm ${
              comment.myReaction === "dislike" ? "text-red-400" : "text-zinc-400 hover:text-red-400"
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
