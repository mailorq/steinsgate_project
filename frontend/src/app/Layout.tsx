import { Outlet } from "react-router-dom";

import { Footer } from "@/shared/ui/Footer";
import { Header } from "@/shared/ui/Header";

export function Layout() {
  return (
    <div className="min-h-screen text-white">
      <Header />

      <main className="pt-16 md:pt-24">
        <div className="mx-auto min-h-screen max-w-[84rem] bg-zinc-900/95 px-3 py-4 md:px-6 md:py-8">
          <Outlet />
        </div>
      </main>

      <Footer />
    </div>
  );
}
