import { useEffect, useRef, useState } from "react";
import type { ChangeEvent, FormEvent } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";

import { ApiError, profileApi } from "@/shared/api";
import { useSession } from "@/shared/session/SessionContext";
import { Avatar } from "@/shared/ui/Avatar";
import { FormCard } from "@/shared/ui/FormCard";

const ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".webp"];
const MAX_AVATAR_SIZE = 8 * 1024 * 1024;

export function ChangeAvatarPage() {
  const navigate = useNavigate();
  const { user, isLoading, setUser } = useSession();
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const previewUrlRef = useRef<string | null>(null);

  useEffect(() => {
    document.title = "Change Avatar";
    return () => {
      if (previewUrlRef.current) {
        URL.revokeObjectURL(previewUrlRef.current);
      }
    };
  }, []);

  if (isLoading) {
    return null;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const selected = event.target.files?.[0] ?? null;
    setError(null);

    if (!selected) {
      setFile(null);
      return;
    }
    if (selected.size > MAX_AVATAR_SIZE) {
      setError("File too large. Max 8 MB");
      return;
    }
    const extension = selected.name.slice(selected.name.lastIndexOf(".")).toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(extension)) {
      setError("Only JPG, PNG, GIF, WEBP allowed");
      return;
    }

    if (previewUrlRef.current) {
      URL.revokeObjectURL(previewUrlRef.current);
    }
    const url = URL.createObjectURL(selected);
    previewUrlRef.current = url;
    setFile(selected);
    setPreviewUrl(url);
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!file) {
      setError("Выберите файл");
      return;
    }

    setIsSubmitting(true);
    setError(null);
    try {
      const updated = await profileApi.uploadAvatar(file);
      setUser(updated);
      navigate("/profile");
    } catch (requestError) {
      setError(
        requestError instanceof ApiError ? requestError.message : "Не удалось выполнить запрос",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <FormCard title="Change Avatar" maxWidthClass="max-w-md">
      <p className="mb-6 text-center text-sm leading-relaxed text-zinc-500">
        Update your Lab Member ID photo. Make it count.
      </p>

      <div className="mb-6 flex justify-center">
        <Avatar
          avatarUrl={previewUrl ?? user.avatar_url}
          username={user.username}
          sizeClass="w-32 h-32"
          textSizeClass="text-5xl"
        />
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-6">
        <div className="w-full">
          <label className="mb-2 block text-lg" htmlFor="avatar">
            Select Image
          </label>
          <input
            type="file"
            id="avatar"
            accept="image/*"
            onChange={handleFileChange}
            className="w-full rounded-lg border border-zinc-800 bg-zinc-900/80 px-4 py-3 text-sm text-zinc-300 transition-colors file:mr-4 file:cursor-pointer file:rounded-lg file:border-0 file:bg-zinc-800 file:px-4 file:py-2 file:text-sm file:font-medium file:text-zinc-200 hover:border-zinc-700 hover:file:bg-zinc-700 focus:border-amber-500/70 focus:outline-none"
          />
          {error && <div className="mt-1 text-sm text-red-500">{error}</div>}
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full rounded-lg bg-amber-500 px-5 py-3.5 text-sm font-semibold text-zinc-950 transition-all duration-200 hover:bg-amber-400 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-40"
        >
          Upload Avatar
        </button>
      </form>

      <div className="mt-6 text-center">
        <Link to="/profile" className="text-sm text-amber-400 transition-colors hover:text-amber-300">
          Back to Settings
        </Link>
      </div>
    </FormCard>
  );
}
