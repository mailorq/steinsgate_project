import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { authApi } from "@/shared/api";
import { useSession } from "@/shared/session/SessionContext";
import { FormCard } from "@/shared/ui/FormCard";

export function LogoutPage() {
  const navigate = useNavigate();
  const { setUser } = useSession();
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    document.title = "Logout";
  }, []);

  async function handleLogout() {
    setIsSubmitting(true);
    try {
      await authApi.logout();
    } finally {
      setUser(null);
      setIsSubmitting(false);
      navigate("/steins-gate");
    }
  }

  return (
    <FormCard title="🚪 Logout" maxWidthClass="max-w-[40rem]">
      <p className="mb-8 text-center text-lg text-zinc-400">Are you sure you want to log out?</p>
      <div className="text-center">
        <button
          type="button"
          onClick={handleLogout}
          disabled={isSubmitting}
          className="rounded-xl bg-red-600 px-10 py-4 text-lg font-semibold text-white transition hover:opacity-80 disabled:cursor-not-allowed disabled:opacity-40"
        >
          Logout
        </button>
      </div>
    </FormCard>
  );
}
