import { useState } from "react";

import { FAQ_QUESTIONS } from "@/shared/config/animes";

export function Faq() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="mx-auto mt-12 mb-6 max-w-[80rem] px-3 md:mt-24 md:mb-10 md:px-6">
      <div className="rounded-xl bg-zinc-800/80 p-4 md:p-8">
        <button
          type="button"
          onClick={() => setIsOpen((open) => !open)}
          className="flex w-full items-center justify-between text-left text-xl font-bold md:text-3xl"
        >
          <span>F.A.Q.</span>
          <span
            className={`text-lg text-red-500 transition-transform duration-300 md:text-2xl ${isOpen ? "rotate-180" : ""}`}
          >
            ˅
          </span>
        </button>

        <div
          className={`grid transition-all duration-500 ease-in-out ${isOpen ? "grid-rows-[1fr]" : "grid-rows-[0fr]"}`}
        >
          <div className="overflow-hidden">
            <div className="mt-4 space-y-3 md:mt-8 md:space-y-6">
              {FAQ_QUESTIONS.map((question) => (
                <a
                  key={question.url}
                  href={question.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block rounded-xl bg-zinc-900 p-3 text-sm transition hover:bg-zinc-800 md:p-5 md:text-base"
                >
                  {question.label}
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
