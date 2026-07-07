import { useState } from "react";

import { FAQ_QUESTIONS } from "@/shared/config/animes";

export function Faq() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="mx-auto mt-14 mb-6 max-w-4xl px-3 md:mt-20 md:px-0">
      <div className="rounded-2xl border border-zinc-800/80 bg-zinc-950/60 p-5 backdrop-blur-sm md:p-7">
        <button
          type="button"
          onClick={() => setIsOpen((open) => !open)}
          className="flex w-full items-center justify-between text-left"
        >
          <span className="text-lg font-semibold tracking-tight md:text-xl">F.A.Q.</span>
          <span
            className={`text-base text-amber-500 transition-transform duration-300 md:text-lg ${isOpen ? "rotate-180" : ""}`}
          >
            ˅
          </span>
        </button>

        <div
          className={`grid transition-all duration-300 ease-out ${isOpen ? "grid-rows-[1fr]" : "grid-rows-[0fr]"}`}
        >
          <div className="overflow-hidden">
            <div className="mt-5 space-y-2">
              {FAQ_QUESTIONS.map((question) => (
                <a
                  key={question.url}
                  href={question.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group flex items-center justify-between rounded-xl border border-transparent bg-zinc-900/60 px-4 py-3 text-sm text-zinc-300 transition-all duration-200 hover:border-zinc-700 hover:text-zinc-100 md:text-base"
                >
                  {question.label}
                  <span className="text-zinc-600 transition-all duration-200 group-hover:translate-x-0.5 group-hover:text-amber-500">
                    →
                  </span>
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
