import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { Link } from "react-router-dom";

import { ApiPendingNotice } from "@/shared/ui/ApiPendingNotice";
import { FormCard } from "@/shared/ui/FormCard";
import { TextField } from "@/shared/ui/TextField";

export function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    document.title = "Login";
  }, []);

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!username.trim() || !password) {
      setError("Введите логин и пароль");
      return;
    }
    setError(null);
    // TODO(api): POST /api/auth/login, обновить сессию и перейти на /steins-gate
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

        <ApiPendingNotice />

        <button
          type="submit"
          className="w-full rounded-xl bg-lime-600 px-9 py-5 text-lg font-semibold text-white transition duration-300 hover:opacity-80"
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
