interface AvatarProps {
  avatarUrl: string | null;
  username: string;
  sizeClass: string;
  textSizeClass?: string;
}

export function Avatar({ avatarUrl, username, sizeClass, textSizeClass = "text-3xl" }: AvatarProps) {
  if (avatarUrl) {
    return (
      <img
        src={avatarUrl}
        alt={`Аватар ${username}`}
        className={`${sizeClass} rounded-full object-cover ring-1 ring-zinc-700`}
      />
    );
  }

  return (
    <div
      className={`${sizeClass} ${textSizeClass} flex items-center justify-center rounded-full bg-gradient-to-br from-zinc-800 to-zinc-900 font-semibold text-amber-500/90 ring-1 ring-zinc-700`}
    >
      {username.charAt(0).toUpperCase()}
    </div>
  );
}
