export interface AnimePlayer {
  label: string;
  src: string;
}

export interface AnimeInfo {
  slug: string;
  name: string;
  /** Короткое имя для меню «Линии» */
  menuLabel: string;
  /** Число мировой линии на divergence-метре */
  worldline: string;
  season: string;
  type: string;
  genres: string;
  description: string;
  poster: string;
  players: AnimePlayer[];
}

export const ANIMES: AnimeInfo[] = [
  {
    slug: "steins-gate",
    name: "Steins;Gate",
    menuLabel: "Steins;Gate",
    worldline: "0.337187",
    season: "2011 весна",
    type: "ТВ (25 эп.), 25 мин.",
    genres:
      "Триллер, Фантастика, Научная фантастика, Тайна, Психологический хоррор, Приключение, Романтика",
    description:
      "В Вратах Штейна рассказывается о группе молодых студентов-технарей. " +
      "Студенты находят способ менять прошлое по почте с помощью модифицированной микроволновки и начинают опыты с целью узнать, " +
      "насколько далеко сможет зайти их открытие, но в итоге все начинает выходить из-под контроля, " +
      "и студенты впутываются в заговор вокруг SERN — организации, стоящей за Большим адронным коллайдером — и Джона Титора, " +
      "утверждающего, что он явился из антиутопичного будущего.",
    poster: "/img/poster_1.webp",
    players: [
      {
        label: "Плеер 1",
        src: "https://www.anilibria.tv/public/iframe.php?id=8674",
      },
      {
        label: "Плеер 2",
        src: "//kodikplayer.com/serial/27423/9bc813cf9293f1305ce036b03845618a/720p?translations=false",
      },
    ],
  },
  {
    slug: "steins-gate-kyoukaimenjou-no-missing-link",
    name: "Steins;Gate: Kyoukaimenjou no Missing Link",
    menuLabel: "Серия 23β",
    worldline: "1.130205",
    season: "2015 зима",
    type: "24 мин.",
    genres: "Триллер, Путешествия во времени, Тайна, Психология, Романтика, Драма",
    description:
      "Специальный эпизод, включенный в Blu-ray издание Steins;Gate Complete. " +
      "Альтернативное завершение Steins;Gate, повествующее о событиях, происходивших в поле аттрактора β. " +
      "Окабe не получает послания из будущего, что подводит к началу истории Steins;Gate 0.",
    poster: "/img/poster_4.webp",
    players: [
      {
        label: "Плеер 1",
        src: "https://kodikplayer.com/video/86794/6ea90a51ef578ff1a7bcabee705613fc/720p",
      },
    ],
  },
  {
    slug: "steins-gate-zero",
    name: "Steins;Gate 0",
    menuLabel: "Steins;Gate 0",
    worldline: "1.129848",
    season: "2018 весна",
    type: "ТВ (24 эп.), 25 мин.",
    genres:
      "Триллер, Фантастика, Научная фантастика, Тайна, Психологический хоррор, Психология, Романтика",
    description:
      "Альтернативная концовка Врат Штейна, " +
      "в которой эгоцентричный безумный ученый Окабе Ринтаро изо всех сил старается оправиться от неудачной попытки спасти жизнь Курису Макисе. " +
      "Стараясь забыть прошлое, Окабе отказывается от своего альтер-эго. И когда, казалось бы, всё наладилось, он снова сталкивается со своим прошлым. " +
      "Он знакомится с девушкой, которая представилась знакомой Курису. " +
      "От неё Окабе узнает, что в данный момент проходит испытание устройства, которое способно воссоздавать характер и личность человека по воспоминаниям. " +
      "Начиная тестирование он и не предполагал, что воссоздание Курису принесет столько мучений и новых неожиданных последствий...",
    poster: "/img/poster_2.webp",
    players: [
      {
        label: "Плеер 1",
        src: "https://www.anilibria.tv/public/iframe.php?id=6140",
      },
      {
        label: "Плеер 2",
        src: "//kodikplayer.com/serial/10115/68d9f5d02225e165c1e650faecfaa3d8/720p?translations=false",
      },
    ],
  },
  {
    slug: "steins-gate-load-region-of-deja-vu",
    name: "Steins;Gate: Load Region of Deja Vu",
    menuLabel: "Фильм",
    worldline: "1.048596",
    season: "2013 весна",
    type: "Фильм, 90 мин.",
    genres: "Триллер, Фантастика, Научная фантастика, Тайна, Психология, Романтика, Драма",
    description:
      "Сюжет фильма разворачивается спустя год после событий сериала. " +
      "Ринтаро Окабe преследуют болезненные воспоминания. " +
      "Зациклившись на созданных им временных линиях, постоянно думая о том, где он совершил ошибку и что сделал неправильно, юноша все больше и больше теряет связь с реальностью. " +
      "В итоге все эти воспоминания становятся причиной стирания его личности из пространственно-временного континуума. " +
      "Тем временем Курису Макисe возвращается в Японию после годового отсутствия. О том, что ее любимый человек действительно существовал, ей подсказывает постоянно возникающее чувство дежавю. " +
      "Этот феномен не дает ей покоя, и она изо всех сил пытается найти способ, чтобы вернуть Окабe.",
    poster: "/img/poster_3.webp",
    players: [
      {
        label: "Плеер 1",
        src: "https://www.anilibria.tv/public/iframe.php?id=543",
      },
      {
        label: "Плеер 2",
        src: "https://kodikplayer.com/video/20557/82311913135640b736d05a065bf8194a/720p",
      },
    ],
  },
];

export function findAnimeBySlug(slug: string | undefined): AnimeInfo | undefined {
  return ANIMES.find((anime) => anime.slug === slug);
}

export interface FaqQuestion {
  label: string;
  url: string;
}

export const FAQ_QUESTIONS: FaqQuestion[] = [
  { label: "Первоисточник", url: "https://steins-gate.fandom.com/wiki/List_of_Steins;Gate_games" },
  { label: "Мировые линии", url: "https://steins-gate.fandom.com/wiki/World_Line" },
  {
    label: "Список известных мировых линий",
    url: "https://steins-gate.fandom.com/wiki/List_of_Known_World_Lines",
  },
  { label: "СЕРН", url: "https://steins-gate.fandom.com/wiki/SERN" },
  {
    label: "Конвергенция мировых линий",
    url: "https://steins-gate.fandom.com/wiki/World_Line_Convergence",
  },
  { label: "Поля аттракторов", url: "https://steins-gate.fandom.com/wiki/Attractor_Field" },
  { label: "Считывающий Штейнер", url: "https://steins-gate.fandom.com/wiki/Reading_Steiner" },
  {
    label: "Теории перемещения во времени",
    url: "https://steins-gate.fandom.com/wiki/Time-travel_theories",
  },
  { label: "Раундеры", url: "https://steins-gate.fandom.com/wiki/Rounders" },
  { label: "Ди-мейлы", url: "https://steins-gate.fandom.com/wiki/D-Mail" },
];
