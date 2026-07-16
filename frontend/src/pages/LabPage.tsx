import { useEffect } from "react";
import { Link } from "react-router-dom";

import { ANIMES } from "@/shared/config/animes";

const WATCH_ORDER = [
  "Смотрите первые 22 серии первого сезона.",
  "Смотрите серию 23β, она является приквелом ко второму сезону «Врата Штейна 0». Этот момент действительно важен.",
  "Смотрите 1-23 серии «Врат Штейна 0». 24-я серия не несёт смысловой нагрузки относительно сюжета.",
  "Смотрите 23-24 серии первого сезона. 25-я серия является спин-оффом.",
  "Смотрите фильм «Врата Штейна: Зона загрузки дежавю», это эпилог, который кратко рассказывает о судьбе главных героев после окончания основного сюжета.",
];

const STATS = [
  { value: "Врата Штейна", caption: "Доступно к просмотру" },
  { value: "Врата Штейна 0", caption: "Доступно к просмотру" },
  { value: "Фильм", caption: "Доступен к просмотру" },
  { value: "Серия 23β", caption: "Доступна к просмотру" },
];

export function LabPage() {
  useEffect(() => {
    document.title = "Future Gadget Laboratory";
  }, []);

  return (
    <>
      <div className="mx-auto mt-2 mb-10 max-w-5xl">
        <div className="rounded-2xl border border-zinc-800/80 bg-zinc-950/60 p-7 backdrop-blur-sm md:p-9">
          <p className="mb-4 font-mono text-xs tracking-[0.25em] text-amber-500/80 uppercase">
            О проекте
          </p>

          <h2 className="mb-5 text-2xl leading-snug font-semibold tracking-tight text-zinc-100">
            Фан-платформа для просмотра Врат Штейна,
            <br />
            созданная как пет-проект
          </h2>

          <div className="space-y-3 leading-relaxed text-zinc-400">
            <p>
              Сайт был создан в рамках пет-проекта, чтобы показать, как работает настоящее
              веб-приложение изнутри: регистрация, подтверждение почты, загрузка файлов, хранение
              данных.
              <br />
              Тайтл выбран намеренно, как один из самых популярных и лично мной любимых. Один
              сериал, никакой лишней сложности, весь фокус на функциональности.
            </p>
            <p>
              Подробнее о функционале сайта можно посмотреть на GitHub. Здесь же я хочу рассказать о
              порядке просмотра и предупреждениях перед ним.
            </p>
            <p>
              Начну с того, что начало аниме достаточно скучное, особенно если вы до этого не
              смотрели ничего подобного, так было и на моём опыте.
              <br />
              Первые 11 серий содержат очень много важной и действительно интересной информации, но,
              вероятно, она станет таковой уже после повторного просмотра.
              <br />
              Также скажу, что тайтл довольно сложный сам по себе, не получится поставить его на фон
              и ни разу не вдуматься в сюжет. Но, по моему субъективному мнению, это только плюс.
              <br />
              Если вы выдержите «духоту» до первого и самого большого сюжетного поворота в 12-й
              серии, вероятно, досмотрите аниме до конца за 1-2 дня.
            </p>
            <p>
              Поэтому хочу посоветовать правильный порядок просмотра, который даст максимум
              впечатлений без спойлеров от самого сюжета:
            </p>
            <ul className="space-y-1.5 pl-1 text-zinc-400">
              {WATCH_ORDER.map((step, index) => (
                <li key={index} className="flex gap-2">
                  <span className="shrink-0 font-mono text-amber-400/60">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  {step}
                </li>
              ))}
            </ul>
            <p className="text-zinc-300">Хорошего просмотра!</p>
          </div>

          <div className="my-6 h-px w-8 bg-amber-400/30" />

          <div className="flex flex-wrap gap-x-10 gap-y-4">
            {STATS.map((stat) => (
              <div key={stat.value} className="flex flex-col gap-0.5">
                <span className="font-mono text-sm text-amber-400">{stat.value}</span>
                <span className="text-xs text-zinc-500">{stat.caption}</span>
              </div>
            ))}
            <a href="https://donatello.to/mailorq" target="_blank" rel="noopener noreferrer">
              <div className="flex flex-col gap-0.5">
                <span className="font-mono text-sm text-amber-400">Поддержка создателей</span>
                <span className="text-xs text-zinc-500">Всегда большое спасибо</span>
              </div>
            </a>
          </div>
        </div>
      </div>

      <div className="mx-auto mt-8 mb-10 max-w-5xl">
        <div className="rounded-2xl border border-zinc-800/80 bg-zinc-950/60 p-6 backdrop-blur-sm md:p-8">
          <h3 className="mb-6 text-xl font-semibold tracking-tight text-zinc-100">Все серии</h3>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
            {ANIMES.map((anime) => (
              <Link
                key={anime.slug}
                to={`/${anime.slug}`}
                className="flex h-full flex-col rounded-xl border border-zinc-800/70 bg-zinc-900/50 p-5 transition-all duration-200 hover:-translate-y-0.5 hover:border-amber-500/40 hover:bg-zinc-900"
              >
                <h4 className="mb-3 text-base font-semibold text-zinc-200">{anime.name}</h4>
                <div className="mt-auto flex items-center justify-between pt-3 text-sm">
                  <span className="text-zinc-400">Мировая линия:</span>
                  <span className="font-mono text-amber-400">{anime.worldline}</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
