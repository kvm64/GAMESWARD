# CONTRIBUTING — Как добавить свою игру в GAMESWARD

Документ для студентов, которые хотят добавить **свою настольную игру** в GAMESWARD.

> 🚀 **Первый раз?** Сначала прочитай **[FORK_GUIDE.md](FORK_GUIDE.md)** — как форкнуть проект.

---

## 🎯 Общая схема

```
1. Форк      → github.com/<твой-логин>/GAMESWARD
2. Клон      → git clone https://github.com/<твой-логин>/GAMESWARD.git
3. Upstream  → git remote add upstream https://github.com/kvm64/GAMESWARD.git
4. Ветка     → git checkout -b feature/<имя-игры>
5. Работа    → движок + компонент + тесты + docs
6. Защита    → показать преподавателю
7. PR        → Pull Request в kvm64/GAMESWARD
8. Ревью     → модератор/преподаватель
9. Merge     → твоя игра в main!
```

**Ключевое правило:** ты работаешь в **своём форке**. Основной репозиторий `kvm64/GAMESWARD` — **не твой**, ты туда пишешь **только через Pull Request**.

---

## 📋 Что нужно добавить (минимум)

### 1. Движок игры

**Файл:** `services/games/<имя_игры>.py`

Наследник `GameEngine`. Реализует:
- `get_initial_state()` — начальная позиция
- `is_valid_move(state, from, to)` — проверка хода
- `apply_move(state, from, to)` — применение хода
- `check_winner(state)` — определение победителя
- (плюс свойства `game_type`, `game_name`, `players_count`)

**Образец:** `services/games/tictactoe.py` (простой), `services/games/russian_checkers.py` (сложный).

### 2. Регистрация в фабрике

**Файл:** `services/games/factory.py`

Добавь:
```python
from .<имя_игры> import <ИмяИгры>Engine

_engines = {
    ...
    '<game_type>': <ИмяИгры>Engine,
}
```

После этого игра **автоматически** появится в списке доступных (API тянет список из фабрики).

### 3. React-компонент

**Файл:** `frontend/src/pages/<ИмяИгры>.jsx`

Пример (для простой игры):
```jsx
import React, { useState, useEffect } from 'react';

export default function MyGame({ gameId, initialState }) {
  const [state, setState] = useState(initialState);

  useEffect(() => {
    if (initialState) setState(initialState);
  }, [initialState]);

  // ... polling, обработка ходов, отрисовка
}
```

**Образец:** `frontend/src/pages/TicTacToe.jsx`.

### 4. Рендер в App.js

**Файл:** `frontend/src/App.js`

Добавь импорт:
```jsx
import MyGame from './pages/MyGame';
```

И рендер:
```jsx
{gameId && gameType === '<game_type>' && gameState && (
  <MyGame gameId={gameId} initialState={gameState} />
)}
```

### 5. Тесты

**Файл:** `services/games/tests/test_<имя_игры>.py`

**Обязательно.** Минимум — 5 тестов:
- Начальная позиция корректна
- Простой ход работает
- Неверный ход отклоняется
- Проверка победы
- Граничный случай (специфичный для твоей игры)

### 6. Документация

**Файл:** `docs/games/<game_type>.md`

По шаблону `docs/games/README.md`.

---

## 🚫 Что запрещено

- ❌ **Пароли, токены, `SECRET_KEY`** — ни в коде, ни в коммитах
- ❌ **`.env`** — не коммитится (в `.gitignore`)
- ❌ **`db.sqlite3`** — не коммитится
- ❌ **`node_modules/`, `.venv/`** — не коммитятся
- ❌ **Копирование чужой игры** — у каждого своя
- ❌ **Игры без тестов** — PR не принимается

---

## 🎨 Стиль коммитов

Используй **conventional commits**:

| Префикс | Когда |
|---------|-------|
| `feat:` | Новая функциональность |
| `fix:` | Исправление бага |
| `docs:` | Документация |
| `test:` | Тесты |
| `refactor:` | Рефакторинг |
| `chore:` | Рутина (обновление зависимостей) |

**Примеры:**
```
feat: add atomic chess engine skeleton
feat: implement explosion logic for atomic chess
test: add tests for pawn exceptions in atomic chess
docs: describe atomic chess rules and limitations
fix: correct king capture validation in atomic chess
```

**Маленькие коммиты лучше больших.** Не «сделал всё», а «сделал шаг 1», «сделал шаг 2».

---

## 🔄 Как работать с upstream

Периодически подтягивай обновления из основного репозитория:

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

Потом — перебазируй свою ветку:
```bash
git checkout feature/<имя-игры>
git rebase main
```

---

## 🆘 Если застрял

1. **Прочитай ошибку** — часто там прямо написано, что не так
2. **Проверь:**
   - Активировано ли `.venv`?
   - Применены ли миграции (`python manage.py migrate`)?
   - Установлены ли зависимости (`pip install -r requirements.txt`, `npm install`)?
3. **Собери «анамнез»** (см. ниже) и **спроси**:
   - преподавателя,
   - ИИ-помощника (через преподавателя),
   - товарища.

### Шаблон «анамнеза» для вопроса

```
Проект: GAMESWARD, ветка feature/my-game, коммит abc1234
Что делаю: реализую проверку хода для игры «Моя игра»
Что ожидаю: метод is_valid_move возвращает True для легального хода
Что получил: исключение IndexError
Что пробовал: проверил границы доски, добавил отладочные print
Файлы: services/games/my_game.py (строки 45-60)
```

⚠️ **Не присылай:**
- Пароли, токены, `.env`
- `db.sqlite3`
- Личные данные

---

## 🏆 Критерии приёмки PR

- [ ] Движок наследует `GameEngine`
- [ ] Игра зарегистрирована в `factory.py`
- [ ] React-компонент работает
- [ ] Тесты написаны и проходят (`python manage.py test`)
- [ ] Документация в `docs/games/<game_type>.md`
- [ ] Нет запрещённых файлов (`.env`, `db.sqlite3`, ...)
- [ ] Коммиты по стилю
- [ ] Игра **не ломает** другие игры

---

## 👥 Роли

| Роль | Кто | Что делает |
|------|-----|-----------|
| **Автор проекта** | Преподаватель | Финальное ревью и merge |
| **Ментор** | Преподаватель + ИИ | Советы, разбор проблем |
| **Модератор** | Лучшие студенты | Первичное ревью PR |
| **Автор игры** | Ты | Движок + компонент + тесты + docs |

---

## 📚 Полезные ссылки

- **GAMESWARD:** https://github.com/kvm64/GAMESWARD
- **ROADMAP:** `docs/ROADMAP.md`
- **Технические решения:** `docs/TECH_DECISIONS.md`
- **Шаблон описания игры:** `docs/games/README.md`

---

**Удачи!** 🚀 Твоя игра может стать частью GAMESWARD и остаться здесь **на годы**.