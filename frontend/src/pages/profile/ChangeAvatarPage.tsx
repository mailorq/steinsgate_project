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
    <FormCard title="Change Avatar" maxWidthClass="max-w-[30rem]">
      <p className="mb-6 text-center italic text-zinc-400">
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
            className="w-full rounded-lg bg-zinc-900/95 px-5 py-4 text-white file:mr-4 file:cursor-pointer file:rounded-lg file:border-0 file:bg-zinc-700 file:px-4 file:py-2 file:font-semibold file:text-white hover:file:bg-zinc-600 focus:ring-2 focus:ring-yellow-400 focus:outline-none"
          />
          {error && <div className="mt-1 text-sm text-red-500">{error}</div>}
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full rounded-xl bg-lime-600 px-9 py-5 text-lg font-semibold text-white transition duration-300 hover:opacity-80 disabled:cursor-not-allowed disabled:opacity-40"
        >
          Upload Avatar
        </button>
      </form>

      <div className="mt-6 text-center">
        <Link to="/profile/settings" className="text-lg text-yellow-400 hover:underline">
          Back to Settings
        </Link>
      </div>
    </FormCard>
  );
}
