import re

from better_profanity import profanity

# Английский словарь — только жесткая лексика, чтобы не блокировать
# эмоциональные damn/hell/crap
EN_PROFANITY = [
    "fuck", "fucking", "fucker", "motherfucker", "bitch", "cunt",
    "faggot", "nigger", "nigga", "asshole", "whore", "slut", "retard",
]
profanity.load_censor_words(EN_PROFANITY)

# Русские корни матчатся от границы слова с необязательной приставкой:
# подстрочный поиск дает ложные срабатывания на обычных словах
RU_PREFIX = r"(?:на|за|до|от|вы|по|под|при|про|раз|рас|съ|у|о|об)?"
RU_ROOTS = [
    "хуй", "хуя", "хуе", "хуёв", "пизд", "ебан", "ёбан", "ебат", "ебал",
    "ебуч", "ебл", "бляд", "блят", "мудак", "мудил", "пидор", "пидар",
    "гандон", "шлюх", "уебк", "уёбк", "уебок", "долбоеб", "далбаеб",
]
RU_WORDS = ["сука", "суки", "сучка", "дебил", "даун", "дауны", "лох", "чмо", "мразь", "тварь"]

_RU_ROOT_RE = re.compile(r"\b" + RU_PREFIX + r"(?:" + "|".join(RU_ROOTS) + r")\w*", re.IGNORECASE)
_RU_WORD_RE = re.compile(r"\b(?:" + "|".join(RU_WORDS) + r")\b", re.IGNORECASE)

_EMOJI_RE = re.compile(
    "[\U0001f000-\U0001faff☀-➿⬀-⯿️‍]"
)
_LEET_RU = str.maketrans({"0": "о", "3": "з", "@": "а", "$": "с", "ё": "е"})

MAX_EMOJI = 12
MAX_CHAR_RUN = 4
VOWELS = set("аеёиоуыэюяaeiouy")


def _letters(text: str) -> str:
    return "".join(ch for ch in text if ch.isalpha()).lower()


def _has_profanity(text: str) -> bool:
    lowered = text.lower().translate(_LEET_RU)
    if _RU_ROOT_RE.search(lowered) or _RU_WORD_RE.search(lowered):
        return True
    return profanity.contains_profanity(lowered)


def _has_long_char_run(text: str) -> bool:
    without_emoji = _EMOJI_RE.sub("", text)
    return re.search(r"(.)\1{" + str(MAX_CHAR_RUN) + r",}", without_emoji) is not None


def _is_mostly_symbols(text: str) -> bool:
    visible = [ch for ch in text if not ch.isspace()]
    if len(visible) < 5:
        return False
    meaningful = sum(1 for ch in visible if ch.isalnum()) + len(_EMOJI_RE.findall(text))
    return meaningful / len(visible) < 0.3


def _is_repeated_pattern(text: str) -> bool:
    letters = _letters(text)
    for size in (2, 3, 4):
        if len(letters) >= size * 3:
            block = letters[:size]
            repeats, tail = divmod(len(letters), size)
            if letters == block * repeats + block[:tail]:
                return True
    return False


def _is_keyboard_mash(text: str) -> bool:
    words = [w for w in re.findall(r"[^\W\d_]+", text.lower()) if len(w) >= 6]
    if not words:
        return False
    mash = [w for w in words if sum(1 for ch in w if ch in VOWELS) / len(w) < 0.15]
    return len(mash) * 2 > len(words)


def check_comment(text: str) -> str | None:
    """Возвращает причину отклонения либо None, если текст допустим."""
    emoji_count = len(_EMOJI_RE.findall(text))
    letters = _letters(text)

    if emoji_count > MAX_EMOJI:
        return "Слишком много эмодзи"

    if not letters:
        # Чисто эмодзи-реакция в пределах лимита допустима
        if emoji_count > 0 and not _is_mostly_symbols(_EMOJI_RE.sub("", text)):
            return None
        return "Комментарий не содержит текста"

    if _has_profanity(text):
        return "Комментарий содержит недопустимую лексику"

    if _has_long_char_run(text):
        return "Слишком много повторяющихся символов"

    if _is_mostly_symbols(text):
        return "Комментарий состоит почти из одних символов"

    if _is_repeated_pattern(text):
        return "Комментарий выглядит как повторяющийся набор символов"

    if _is_keyboard_mash(text):
        return "Комментарий выглядит как бессмысленный набор букв"

    return None
