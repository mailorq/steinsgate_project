import { Outlet, useLocation } from "react-router-dom";

import { Footer } from "@/shared/ui/Footer";
import { Header } from "@/shared/ui/Header";

export function Layout() {
  const { pathname } = useLocation();

  return (
    <div className="min-h-screen text-zinc-100">
      <Header />

      <main className="pt-20 md:pt-24">
        <div key={pathname} className="page-enter mx-auto min-h-screen max-w-6xl px-3 py-4 md:px-6 md:py-8">
          <Outlet />
        </div>
      </main>

      <Footer />
    </div>
  );
}
