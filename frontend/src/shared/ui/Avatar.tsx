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
        className={`${sizeClass} rounded-full object-cover ring-2 ring-yellow-400`}
      />
    );
  }

  return (
    <div
      className={`${sizeClass} ${textSizeClass} flex items-center justify-center rounded-full bg-zinc-900 font-bold ring-2 ring-zinc-600`}
    >
      {username.charAt(0).toUpperCase()}
    </div>
  );
}
