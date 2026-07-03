import { useEffect } from "react";

export function AuthStubPage() {
  useEffect(() => {
    document.title = "Steins;Gate Fan Site";
  }, []);

  return (
    <div className="mx-auto mt-4 mb-10 max-w-[80rem]">
      <div className="rounded-xl bg-zinc-800/80 p-8 text-center">
        <p className="mb-4 font-mono text-xs tracking-[0.2em] text-amber-400/70 uppercase">
          Operation Skuld
        </p>
        <h2 className="text-2xl font-semibold text-zinc-100">
          Авторизация переезжает на новый API
        </h2>
        <p className="mt-3 text-zinc-400">
          Регистрация, вход и профиль вернутся после подключения фронтенда к django-ninja.
        </p>
      </div>
    </div>
  );
}
