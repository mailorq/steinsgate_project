import { useState } from "react";

interface SpoilerTextProps {
  text: string;
}

export function SpoilerText({ text }: SpoilerTextProps) {
  const parts = text.split(/\|\|(.+?)\|\|/gs);

  return (
    <>
      {parts.map((part, index) =>
        index % 2 === 1 ? <Spoiler key={index} content={part} /> : part,
      )}
    </>
  );
}

function Spoiler({ content }: { content: string }) {
  const [revealed, setRevealed] = useState(false);

  return (
    <span
      onClick={() => setRevealed(true)}
      role="button"
      tabIndex={revealed ? -1 : 0}
      aria-label={revealed ? undefined : "Показать спойлер"}
      onKeyDown={(event) => event.key === "Enter" && setRevealed(true)}
      className={`relative inline rounded-[4px] px-1 py-0.5 transition-[background-color] duration-500 ${
        revealed ? "cursor-text bg-zinc-500/10" : "cursor-pointer bg-zinc-600/30"
      }`}
    >
      <span
        className={`transition-[filter,opacity] duration-500 ease-out ${
          revealed ? "opacity-100 blur-0" : "opacity-60 blur-[6px] select-none"
        }`}
      >
        {content}
      </span>
    </span>
  );
}
