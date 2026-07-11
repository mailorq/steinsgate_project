// Клиентское зеркало серверных эвристик для мгновенной обратной связи.
// Проверка лексики остается на сервере — словарь не выносится в бандл.

const EMOJI_RE = /[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}]/gu;
const EMOJI_JOINERS_RE = /[\u{FE0F}\u{200D}]/gu;

export const MIN_LENGTH = 3;
export const MAX_LENGTH = 900;
const MAX_EMOJI = 12;

function letters(text: string): string {
  return (text.toLowerCase().match(/\p{L}/gu) ?? []).join("");
}

export function checkComment(rawText: string): string | null {
  const text = rawText.trim().replaceAll("||", "").replace(EMOJI_JOINERS_RE, "");
  const emojiCount = (text.match(EMOJI_RE) ?? []).length;
  const textLetters = letters(text);

  if (text.length < MIN_LENGTH) {
    return "Комментарий слишком короткий";
  }
  if (text.length > MAX_LENGTH) {
    return `Комментарий длиннее ${MAX_LENGTH} символов`;
  }
  if (emojiCount > MAX_EMOJI) {
    return "Слишком много эмодзи";
  }

  if (textLetters.length === 0) {
    if (emojiCount > 0) {
      return null;
    }
    return "Комментарий не содержит текста";
  }

  const withoutEmoji = text.replace(EMOJI_RE, "");
  if (/(.)\1{4,}/u.test(withoutEmoji)) {
    return "Слишком много повторяющихся символов";
  }

  const visible = withoutEmoji.replace(/\s/gu, "");
  const meaningful = (visible.match(/[\p{L}\p{N}]/gu) ?? []).length;
  if (visible.length >= 5 && (meaningful + emojiCount) / (visible.length + emojiCount) < 0.3) {
    return "Комментарий состоит почти из одних символов";
  }

  for (const size of [2, 3, 4]) {
    if (textLetters.length >= size * 3) {
      const block = textLetters.slice(0, size);
      const repeated = block.repeat(Math.ceil(textLetters.length / size)).slice(0, textLetters.length);
      if (textLetters === repeated) {
        return "Комментарий выглядит как повторяющийся набор символов";
      }
    }
  }

  return null;
}
