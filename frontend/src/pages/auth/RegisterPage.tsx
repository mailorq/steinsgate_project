import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";

import { ApiPendingNotice } from "@/shared/ui/ApiPendingNotice";
import { FormCard } from "@/shared/ui/FormCard";
import { TextField } from "@/shared/ui/TextField";

interface RegisterErrors {
  username?: string;
  email?: string;
  password?: string;
  confirmPassword?: string;
}

export function RegisterPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errors, setErrors] = useState<RegisterErrors>({});

  useEffect(() => {
    document.title = "Registration";
  }, []);

  function validate(): RegisterErrors {
    const next: RegisterErrors = {};
    if (!username.trim()) {
      next.username = "Введите логин";
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      next.email = "Введите корректный email";
    }
    if (password.length < 8) {
      next.password = "Пароль должен быть не короче 8 символов";
    }
    if (password !== confirmPassword) {
      next.confirmPassword = "Пароли не совпадают";
    }
    return next;
  }

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const next = validate();
    setErrors(next);
    if (Object.keys(next).length > 0) {
      return;
    }
    // TODO(api): POST /api/auth/register, затем переход на подтверждение почты
    navigate("/verify-email");
  }

  return (
    <FormCard
      title="🚪 Registration"
      subtitle="The Future Gadget Laboratory needs you. Rise and become a Lab Member!"
    >
      <form onSubmit={handleSubmit} noValidate className="flex flex-col gap-6">
        <TextField
          id="username"
          label="👤 Login"
          type="text"
          placeholder="Enter login"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          error={errors.username}
        />
        <TextField
          id="email"
          label="📧 Email"
          type="email"
          placeholder="Enter email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          error={errors.email}
        />
        <TextField
          id="password"
          label="🔑 Password"
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          error={errors.password}
        />
        <TextField
          id="confirm-password"
          label="🔑 Confirm Password"
          type="password"
          placeholder="Repeat the password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          error={errors.confirmPassword}
        />

        <ApiPendingNotice />

        <button
          type="submit"
          className="w-full rounded-xl bg-lime-600 px-9 py-5 text-lg font-semibold text-white transition duration-300 hover:opacity-80"
        >
          Register
        </button>
      </form>

      <div className="mt-8 text-center">
        <p className="text-lg text-zinc-400">
          What? You’re already a Lab Member? Then step this way!{" "}
          <Link to="/login" className="text-yellow-400 hover:underline">
            Sign in
          </Link>
        </p>
      </div>
    </FormCard>
  );
}
