import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";

import { ApiError, authApi } from "@/shared/api";
import { useSession } from "@/shared/session/SessionContext";
import { FormCard } from "@/shared/ui/FormCard";
import { TextField } from "@/shared/ui/TextField";

export function LoginPage() {
  const navigate = useNavigate();
  const { setUser } = useSession();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    document.title = "Login";
  }, []);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!username.trim() || !password) {
      setError("Введите логин и пароль");
      return;
    }

    setIsSubmitting(true);
    setError(null);
    try {
      const session = await authApi.login({ username: username.trim(), password });
      setUser(session.user ?? null);
      navigate("/steins-gate");
    } catch (requestError) {
      setError(
        requestError instanceof ApiError ? requestError.message : "Не удалось выполнить запрос",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <FormCard
      title="🔓 Login"
      subtitle="The Reading Steiner seems to be malfunctioning… remind me… what was your name again?"
    >
      <form onSubmit={handleSubmit} noValidate className="flex flex-col gap-6">
        {error && <div className="mb-2 text-center text-sm text-red-500">{error}</div>}

        <TextField
          id="username"
          label="👤 Login"
          type="text"
          placeholder="Enter login"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <TextField
          id="password"
          label="🔑 Password"
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full rounded-xl bg-lime-600 px-9 py-5 text-lg font-semibold text-white transition duration-300 hover:opacity-80 disabled:cursor-not-allowed disabled:opacity-40"
        >
          Sign in
        </button>
      </form>

      <div className="mt-8 text-center">
        <p className="text-lg text-zinc-400">
          Not a lab member yet?! Then here!{" "}
          <Link to="/register" className="text-yellow-400 hover:underline">
            Register
          </Link>
        </p>
      </div>
    </FormCard>
  );
}
