/**
 * Очистка локального хранилища GAMESWARD.
 *
 * Использование в браузере (F12 → Console):
 *   import('./utils/clearStorage.js').then(m => m.clearAll());
 *
 * Или через кнопку в UI (если добавить).
 */

export const clearCurrentGame = () => {
  localStorage.removeItem('currentGame');
  console.log('✅ currentGame очищен');
};

export const clearAuth = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
  console.log('✅ Токены и пользователь очищены');
};

export const clearAll = () => {
  localStorage.clear();
  console.log('✅ Всё локальное хранилище очищено');
};

// Для использования в Console без import:
if (typeof window !== 'undefined') {
  window.gameswardClear = {
    all: clearAll,
    game: clearCurrentGame,
    auth: clearAuth,
  };
}