import { useEffect, useRef, useState } from "react";

const ANIMATION_DURATION_MS = 1000;
const TICK_MS = 40;

interface DivergenceMeterProps {
  /** Число мировой линии, например "0.337187" */
  value: string;
}

export function DivergenceMeter({ value }: DivergenceMeterProps) {
  const [chars, setChars] = useState<string[]>(() => value.split(""));
  const [flickering, setFlickering] = useState<Set<number>>(new Set());
  const intervalRef = useRef<number | null>(null);

  useEffect(() => {
    const target = value.split("");
    const startedAt = Date.now();

    if (intervalRef.current !== null) {
      window.clearInterval(intervalRef.current);
    }

    intervalRef.current = window.setInterval(() => {
      if (Date.now() - startedAt >= ANIMATION_DURATION_MS) {
        window.clearInterval(intervalRef.current!);
        intervalRef.current = null;
        setChars(target);
        setFlickering(new Set());
        return;
      }

      setChars(target.map((char) => (char === "." ? "." : String(Math.floor(Math.random() * 10)))));
      setFlickering(
        new Set(target.map((_, i) => i).filter((i) => target[i] !== "." && Math.random() > 0.8)),
      );
    }, TICK_MS);

    return () => {
      if (intervalRef.current !== null) {
        window.clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [value]);

  return (
    <div className="nixie-container" aria-label={`Мировая линия ${value}`}>
      {chars.map((char, i) =>
        char === "." ? (
          <div key={i} className="nixie-dot">
            .
          </div>
        ) : (
          <div key={i} className={`nixie-digit${flickering.has(i) ? " flicker" : ""}`}>
            {char}
          </div>
        ),
      )}
    </div>
  );
}
