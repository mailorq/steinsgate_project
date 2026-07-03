import { useEffect } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";

import { useSession } from "@/shared/session/SessionContext";

const BUTTON_CLASS =
  "block w-full rounded-xl py-4 text-center text-lg font-semibold text-white transition hover:opacity-80";

export function SettingsPage() {
  const navigate = useNavigate();
  const { user } = useSession();

  useEffect(() => {
    document.title = "Settings";
  }, []);

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="mx-auto mt-8 mb-12 max-w-[30rem] rounded-xl bg-zinc-800/80 p-8 shadow-lg">
      <Link to="/profile/nickname" className={`${BUTTON_CLASS} mt-2 mb-6 bg-blue-600`}>
        Change name
      </Link>
      <Link to="/profile/avatar" className={`${BUTTON_CLASS} mb-10 bg-blue-600`}>
        Change avatar
      </Link>
      <Link to="/profile" className={`${BUTTON_CLASS} mb-10 bg-green-500`}>
        Back to profile
      </Link>
      <button type="button" onClick={() => navigate("/logout")} className={`${BUTTON_CLASS} bg-red-600`}>
        Logout
      </button>
    </div>
  );
}
