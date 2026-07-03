import { useEffect } from "react";
import { Link, Navigate } from "react-router-dom";

import { useSession } from "@/shared/session/SessionContext";
import { Avatar } from "@/shared/ui/Avatar";

export function ProfilePage() {
  const { user } = useSession();

  useEffect(() => {
    document.title = "Profile";
  }, []);

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="mx-auto mt-4 mb-6 max-w-[40rem] rounded-xl bg-zinc-800/80 p-4 shadow-lg md:mt-8 md:mb-12 md:p-10">
      <h2 className="mb-6 text-center text-2xl font-bold md:mb-10 md:text-4xl">👤 Profile</h2>

      <div className="flex flex-col items-center justify-center gap-6 md:flex-row md:gap-10">
        <div className="flex-shrink-0">
          <Avatar
            avatarUrl={user.avatarUrl}
            username={user.username}
            sizeClass="w-32 h-32 md:w-56 md:h-56"
            textSizeClass="text-3xl md:text-5xl"
          />
        </div>

        <div className="flex w-full flex-col justify-center gap-3 text-base md:w-auto md:gap-4 md:text-lg">
          <div>
            <span className="text-sm text-zinc-400 md:text-base">Nickname:</span>
            <p className="text-xl font-semibold break-words md:text-2xl">{user.nickname}</p>
          </div>
          <div>
            <span className="text-sm text-zinc-400 md:text-base">Username:</span>
            <p className="text-xl font-semibold break-words md:text-2xl">{user.username}</p>
          </div>
          <div>
            <span className="text-sm text-zinc-400 md:text-base">Email:</span>
            <p className="text-sm break-all text-zinc-300 md:text-base">{user.email}</p>
          </div>
        </div>
      </div>

      <div className="mt-6 md:mt-10">
        <Link
          to="/profile/settings"
          className="block w-full rounded-xl bg-red-600 py-3 text-center text-base font-semibold text-white transition hover:bg-red-700 md:py-4 md:text-lg"
        >
          Settings
        </Link>
      </div>
    </div>
  );
}
