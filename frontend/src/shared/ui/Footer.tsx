export function Footer() {
  return (
    <footer className="border-t border-zinc-800/70 bg-zinc-950/60 py-8">
      <div className="mx-auto flex max-w-6xl flex-col items-center gap-2 px-4 text-center">
        <p className="font-mono text-sm tracking-widest text-amber-500/80 uppercase">
          El Psy Kongroo
        </p>
        <p className="text-xs text-zinc-500">
          © 2026 Steins;Gate fan site. All Rights Reserved
        </p>
        <p className="text-xs text-zinc-600">steins;gate@example.com</p>
        <p className="text-xs text-zinc-600">
          created by{" "}
          <a
            href="https://mailorq.com"
            target="_blank"
            rel="noopener noreferrer"
            className="text-amber-500/80 transition-colors hover:text-amber-400"
          >
            mailorq
          </a>
        </p>
      </div>
    </footer>
  );
}
