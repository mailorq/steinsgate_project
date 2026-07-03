import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { useSession } from "@/shared/session/SessionContext";
import { FormCard } from "@/shared/ui/FormCard";

export function LogoutPage() {
  const navigate = useNavigate();
  const { logout } = useSession();

  useEffect(() => {
    document.title = "Logout";
  }, []);

  function handleLogout() {
    // TODO(api): POST /api/auth/logout
    logout();
    navigate("/steins-gate");
  }

  return (
    <FormCard title="🚪 Logout" maxWidthClass="max-w-[40rem]">
      <p className="mb-8 text-center text-lg text-zinc-400">Are you sure you want to log out?</p>
      <div className="text-center">
        <button
          type="button"
          onClick={handleLogout}
          className="rounded-xl bg-red-600 px-10 py-4 text-lg font-semibold text-white transition hover:opacity-80"
        >
          Logout
        </button>
      </div>
    </FormCard>
  );
}
