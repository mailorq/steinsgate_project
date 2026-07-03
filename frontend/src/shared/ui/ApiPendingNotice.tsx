/**
 * Временный баннер для действий, которым нужен бэкенд.
 * TODO(api): удалить после подключения django-ninja (фаза 2).
 */
export function ApiPendingNotice() {
  return (
    <div className="rounded-lg border border-amber-400/30 bg-zinc-900 p-4 text-center text-sm text-amber-400/90">
      Действие будет доступно после подключения API (django-ninja, фаза 2).
    </div>
  );
}
