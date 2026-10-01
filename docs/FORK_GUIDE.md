# FORK_GUIDE — Как форкнуть GAMESWARD

Пошаговая инструкция для студентов: от регистрации на GitHub до первого коммита в своём форке.

---

## 🎯 Что такое форк и зачем он нужен

**Форк** — это **твоя собственная копия** репозитория на GitHub.

**Зачем:**
- Ты работаешь **в своей копии** — не мешаешь другим.
- Основной репозиторий `kvm64/GAMESWARD` — **не твой**, ты туда **не пишешь напрямую**.
- Когда закончишь игру — предложишь её через **Pull Request** (PR).

**Как это выглядит:**

```
┌─────────────────────────────────────────┐
│ github.com/kvm64/GAMESWARD              │  ← основной (не трогаешь)
│  main: стабильная версия                │
└──────────────────┬──────────────────────┘
                   │ Fork
                   ▼
┌─────────────────────────────────────────┐
│ github.com/<твой-логин>/GAMESWARD       │  ← твой форк (работаешь тут)
│  feature/<имя-игры>: твоя игра          │
└─────────────────────────────────────────┘
                   │ Pull Request
                   ▼
┌─────────────────────────────────────────┐
│ github.com/kvm64/GAMESWARD              │  ← после ревью → merge
│  main: твоя игра в основном проекте!    │
└─────────────────────────────────────────┘
```

---

## 📝 Шаг 0: Что нужно заранее

- **Аккаунт на GitHub** (если нет — см. Шаг 1)
- **Git** установлен (`git --version` в терминале)
- **Python 3.13+** и **Node.js 18+** (понадобятся позже — см. `SETUP.md`)
- **Редактор кода** (VS Code, PyCharm)

---

## 🔑 Шаг 1: Регистрация на GitHub

**Если аккаунта нет:**

1. Открой https://github.com/signup
2. Введи email, пароль, имя пользователя.
3. Подтверди email.
4. Готово — ты на GitHub.

**Если аккаунт есть** — пропусти этот шаг.

> 💡 **Имя пользователя** (`username`) будет частью ссылки на твой форк: `github.com/<твой-логин>/GAMESWARD`. Выбирай осмысленное.

---

## 🍴 Шаг 2: Форкнуть основной репозиторий

1. Открой в браузере: **https://github.com/kvm64/GAMESWARD**

2. В правом верхнем углу нажми кнопку **«Fork»** (рядом со «Star»).

   ```
   ┌─────────────────────────────────────────────┐
   │  kvm64 / GAMESWARD            ⭐ Star  🍴 Fork │
   └─────────────────────────────────────────────┘
   ```

3. Откроется страница **«Create a new fork»**:
   - **Owner:** выбери **свой аккаунт** (например, `ivan`).
   - **Repository name:** оставь `GAMESWARD`.
   - **Description:** можно оставить пустым.
   - **Copy the `main` branch only:** оставь галочку.

4. Нажми **«Create fork»**.

5. Через 5–10 секунд откроется **твой форк**: `github.com/ivan/GAMESWARD`.

> ⚠️ **Важно:** заголовок страницы теперь содержит **твоё имя**: `ivan / GAMESWARD`, а под ним — `forked from kvm64/GAMESWARD`.

---

## 💻 Шаг 3: Клонировать СВОЙ форк

Открой терминал (PowerShell, Bash) и выполни:

```bash
cd <папка-для-проектов>
git clone https://github.com/<твой-логин>/GAMESWARD.git
cd GAMESWARD
```

**Пример:**
```bash
cd C:\KVM_Projects
git clone https://github.com/ivan/GAMESWARD.git
cd GAMESWARD
```

> ⚠️ **Клонируй СВОЙ форк, а не основной репозиторий.** Иначе не сможешь пушить свои изменения.

**Проверка:**
```bash
git remote -v
```

Должно вывести:
```
origin  https://github.com/<твой-логин>/GAMESWARD.git (fetch)
origin  https://github.com/<твой-логин>/GAMESWARD.git (push)
```

---

## 🔗 Шаг 4: Добавить upstream

**Upstream** — это ссылка на **основной** репозиторий. Она нужна, чтобы **подтягивать** свежие изменения от преподавателя.

```bash
git remote add upstream https://github.com/kvm64/GAMESWARD.git
git fetch upstream
```

**Проверка:**
```bash
git remote -v
```

Теперь должно быть **четыре строки**:
```
origin    https://github.com/<твой-логин>/GAMESWARD.git (fetch)
origin    https://github.com/<твой-логин>/GAMESWARD.git (push)
upstream  https://github.com/kvm64/GAMESWARD.git (fetch)
upstream  https://github.com/kvm64/GAMESWARD.git (push)
```

- **`origin`** — твой форк (сюда пушишь свои изменения).
- **`upstream`** — основной репозиторий (отсюда подтягиваешь обновления).

---

## ⚙️ Шаг 5: Настроить git (один раз)

Если ты **впервые** коммитишь на этом компьютере — настрой имя и email:

```bash
git config user.name "Иван Иванов"
git config user.email "ivan@example.com"
```

> ⚠️ **Email должен совпадать** с тем, что привязан к GitHub. Иначе коммиты не засчитаются в профиль.

**Проверка:**
```bash
git config user.name
git config user.email
```

---

## 🌿 Шаг 6: Создать ветку под свою игру

**Никогда не работай в `main`** — это ветка для стабильной версии. Создай **свою ветку**:

```bash
git checkout -b feature/<имя-игры>
```

**Примеры:**
```bash
git checkout -b feature/atomic-chess
git checkout -b feature/go
git checkout -b feature/shogi
git checkout -b feature/monopoly
```

**Проверка:**
```bash
git branch
```

Должна быть звёздочка напротив твоей ветки:
```
* feature/atomic-chess
  main
```

---

## 🚀 Шаг 7: Развернуть проект

Теперь у тебя есть код — но он **не запущен**. Смотри:

👉 **`docs/SETUP.md`** — пошаговая инструкция: venv, миграции, `npm install`, запуск.

**Кратко:**
```bash
# Бэкенд
python -m venv .venv
.venv\Scripts\Activate.ps1      # Windows
source .venv/bin/activate        # Linux/Mac
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python scripts/create_roles.py
python manage.py runserver

# Фронтенд (второй терминал)
cd frontend
npm install
npm start
```

---

## 🎮 Шаг 8: Начать работу над игрой

**Что делать:**
1. Прочитай **`docs/CONTRIBUTING.md`** — что нужно добавить.
2. Посмотри образцы: `services/games/tictactoe.py`, `frontend/src/pages/TicTacToe.jsx`.
3. Работай **маленькими шагами** — коммить после каждого.

**Минимум для игры:**
- ✅ Движок в `services/games/<game>.py`
- ✅ Регистрация в `services/games/factory.py`
- ✅ React-компонент в `frontend/src/pages/<Game>.jsx`
- ✅ Рендер в `frontend/src/App.js`
- ✅ Тесты в `services/games/tests/test_<game>.py`
- ✅ Описание в `docs/games/<game_type>.md`

---

## 💾 Шаг 9: Коммитить и пушить

**Маленькие коммиты** — лучше больших. После каждого шага:

```bash
git add services/games/atomic_chess.py
git commit -m "feat: add engine skeleton for atomic chess"
git push origin feature/atomic-chess
```

**Стиль коммитов** (см. `CONTRIBUTING.md`):
- `feat:` — новая функциональность
- `fix:` — исправление
- `test:` — тесты
- `docs:` — документация

**Проверка:** зайди на `github.com/<твой-логин>/GAMESWARD` → увидишь свежие коммиты.

---

## 🔄 Шаг 10: Подтягивать обновления (регулярно)

Преподаватель обновляет основной репозиторий. Чтобы **не отставать**:

```bash
# 1. Скачать свежее из upstream
git fetch upstream

# 2. Переключиться на main
git checkout main

# 3. Слить upstream/main в свой main
git merge upstream/main

# 4. Отправить обновлённый main в свой форк
git push origin main

# 5. Вернуться на свою ветку
git checkout feature/atomic-chess

# 6. Перебазировать ветку на свежий main
git rebase main
```

**Делай это раз в 1–2 недели** — иначе будет много конфликтов при PR.

---

## 🆘 Шаг 11: Если застрял

**Теперь у тебя ЕСТЬ форк** — можно обращаться за советом:

| Ситуация                              | Куда идти                                         |
| ------------------------------------- | ------------------------------------------------- |
| Не понимаю правила игры               | `docs/games/<game>.md`                            |
| Проблема с кодом                      | `docs/HOW_TO_ASK.md` → шаблон → преподаватель/чат |
| Ошибка в git                          | Преподаватель / староста                          |
| Вопрос по архитектуре                 | Преподаватель → ИИ-помощник                       |
| Критическая ошибка в основном проекте | Преподаватель                                     |

**Шаблон вопроса** — в `docs/HOW_TO_ASK.md`. **Пароли и `.env` не присылай.**

---

## 🎓 Шаг 12: Pull Request (после защиты)

Когда игра готова и защищена:

1. Открой **свой форк** на GitHub.
2. Увидишь баннер **«feature/atomic-chess had recent pushes — Compare & pull request»**.
3. Нажми **«Compare & pull request»**.
4. Заполни:
   - **Title:** `feat: add atomic chess`
   - **Description:** краткое описание + ссылка на `docs/games/atomic_chess.md`
5. Нажми **«Create pull request»**.
6. Жди ревью от преподавателя или модератора.

**Что проверят:**
- [ ] Движок наследует `GameEngine`
- [ ] Игра зарегистрирована в `factory.py`
- [ ] React-компонент работает
- [ ] Тесты написаны и проходят
- [ ] Есть `docs/games/<game>.md`
- [ ] Нет `.env`, `db.sqlite3`, `node_modules`
- [ ] Коммиты по стилю

---

## 📌 Шпаргалка (для тех, кто уже знает)

```bash
# Разово
git clone https://github.com/<логин>/GAMESWARD.git
cd GAMESWARD
git remote add upstream https://github.com/kvm64/GAMESWARD.git
git config user.name "Имя"
git config user.email "email"

# Каждая новая задача
git fetch upstream && git checkout main && git merge upstream/main
git checkout -b feature/<имя>
# ... работа ...
git add <файлы>
git commit -m "feat: ..."
git push origin feature/<имя>
```

---

## 🚫 Что НЕ делать

- ❌ **Не пушить в `upstream`** — ты не имеешь прав (и не должен).
- ❌ **Не работать в `main`** — только в своей ветке.
- ❌ **Не коммитить `.env`, `db.sqlite3`, `node_modules`** — они в `.gitignore`.
- ❌ **Не присылать пароли** никому — ни преподавателю, ни ИИ.
- ❌ **Не копировать чужую игру** — у каждого своя.

---

## 📚 Ссылки

- **Основной репозиторий:** https://github.com/kvm64/GAMESWARD
- **ROADMAP:** `docs/ROADMAP.md`
- **CONTRIBUTING:** `docs/CONTRIBUTING.md` — что добавить для своей игры
- **SETUP:** `docs/SETUP.md` — как развернуть проект
- **HOW_TO_ASK:** `docs/HOW_TO_ASK.md` — как обращаться с вопросами
- **Шаблон описания игры:** `docs/games/README.md`

---



## 🎯 Два пути: вклад в GAMESWARD или свой проект

После форка у тебя есть **два принципиально разных пути**. Выбери **осознанно** — от этого зависит, как ты работаешь.

### 🅰️ Путь A: Вклад в GAMESWARD (open-source)

**Что делаешь:**
- Оставляешь **все** игры в проекте (tictactoe, russian_checkers).
- **Добавляешь свою** как ещё одну игру.
- Следуешь правилам из `docs/CONTRIBUTING.md`.
- Пишешь **тесты**, **документацию**, коммитишь по стилю.
- В конце — **Pull Request** в `kvm64/GAMESWARD`.

**Результат:** твоя игра **в общем проекте**, ты — **контрибьютор** GAMESWARD.

**Плюсы:**
- ✅ Портфолио в open-source — **реальный вклад** в чужой проект.
- ✅ Твой код **останется** надолго (после merge).
- ✅ Опыт работы с **code review**, PR, git-flow.
- ✅ Строка в резюме: «контрибьютор GAMESWARD».

**Минусы:**
- ⚠️ Нужно следовать **чужим правилам** (тесты, стиль, ревью).
- ⚠️ Твоя игра может быть **отклонена** или **отправлена на доработку**.
- ⚠️ Ты **не владеешь** проектом — им управляет автор (преподаватель).

**Кому подходит:**
- Хочет **портфолио в open-source**.
- Готов **соблюдать правила**.
- Не против, что игра **не его личный проект**.

---

### 🅱️ Путь B: Свой проект на базе GAMESWARD

**Что делаешь:**
- **Берёшь** GAMESWARD как **основу** (архитектура, ядро, API).
- **Убираешь** лишние игры (tictactoe, russian_checkers).
- **Оставляешь только свою** игру.
- Даёшь проекту **своё имя** (например, CHESSWARD, BLOGWARD, MYWARD).
- Работаешь **свободно** — правила GAMESWARD для тебя **не обязательны**.

**Результат:** **твой собственный проект**, выросший из GAMESWARD.

**Плюсы:**
- ✅ **Полная свобода** — меняй что хочешь.
- ✅ **Своя история** — комиссия/работодатель увидит **твой** путь.
- ✅ **Своё имя** — «мой проект CHESSWARD».
- ✅ Можно **развивать** дальше — свой бренд, своя команда.
- ✅ **Не зависишь** от ревью и правил.

**Минусы:**
- ⚠️ Теряешь связь с апстримом (`git pull upstream` не сработает).
- ⚠️ Обновления GAMESWARD **не подтянутся** автоматически.
- ⚠️ **Лицензия GPLv3** — если публикуешь, обязан оставить GPLv3 и упомянуть GAMESWARD.

**Кому подходит:**
- Делает **дипломный проект**.
- Хочет **свой проект** для портфолио.
- Не хочет зависеть от чужого ревью.

---

### 📊 Сравнение

| Критерий                      | Путь A (вклад)   | Путь B (свой)           |
| ----------------------------- | ---------------- | ----------------------- |
| **Цель**                      | Игра в GAMESWARD | Свой проект             |
| **Все игры**                  | Оставляешь       | Убираешь лишние         |
| **Правила CONTRIBUTING**      | Обязательны      | Не обязательны          |
| **Тесты**                     | Обязательны      | По желанию              |
| **PR в upstream**             | Да               | Нет                     |
| **Связь с GAMESWARD**         | Есть             | Теряется                |
| **Имя проекта**               | GAMESWARD        | Своё                    |
| **Для диплома**               | Не идеально      | **Идеально**            |
| **Для open-source портфолио** | **Идеально**     | Возможно                |
| **Лицензия**                  | GPLv3            | GPLv3 (если публикуешь) |

---

### 🛠 Как реализовать Путь B

**1. Форкни GAMESWARD** (см. Шаги 1–5 выше).

**2. Реши, как назвать проект:**
- `CHESSWARD` — если делаешь шахматы.
- `BLOGWARD` — если делаешь блог (по аналогии).
- `MYWARD` — универсальное.

**3. Переименуй форк на GitHub:**
- Settings → Repository name → ввести новое имя → Rename.

**4. Локально переименуй папку:**
```bash
cd ..
mv GAMESWARD MYWARD
cd MYWARD
```

**5. Обнови ссылку на origin:**
```bash
git remote set-url origin https://github.com/<логин>/MYWARD.git
```

**6. Убери лишние игры** (чек-лист ниже).

**7. Убери связь с upstream** (опционально — если не хочешь подтягивать обновления):
```bash
git remote remove upstream
```

**8. Обнови README.md:**
- Название проекта.
- Описание (что это, зачем).
- Упоминание: «На базе GAMESWARD (github.com/kvm64/GAMESWARD)».
- Лицензия GPLv3 (сохрани).

**9. Работай как над своим проектом.** 🚀

---

### 🗑 Чек-лист: что убрать для Пути B

**Игры и компоненты:**
```
services/games/tictactoe.py
services/games/russian_checkers.py
frontend/src/pages/TicTacToe.jsx
frontend/src/pages/RussianCheckers.jsx
frontend/src/pages/Invitations.jsx       # если не нужны приглашения
frontend/src/pages/SelectOpponent.jsx    # если своя логика
docs/games/README.md                     # замени на свой
```

**В `services/games/factory.py`** — убери импорты и строки лишних игр:
```python
from .base import GameEngine
# from .tictactoe import TicTacToeEngine          # убрать
# from .russian_checkers import RussianCheckersEngine  # убрать
from .my_game import MyGameEngine                 # ← твоя игра

_engines = {
    'my_game': MyGameEngine,   # ← оставить только свою
}
```

**В `frontend/src/App.js`** — убери рендер лишних игр:
```jsx
// {gameId && gameType === 'tictactoe' && gameState && (     // убрать
//   <TicTacToe ... />                                       // убрать
// )}                                                        // убрать

{gameId && gameType === 'my_game' && gameState && (
  <MyGame gameId={gameId} initialState={gameState} />
)}
```

**Оставить (обязательно):**
```
core/                    # ядро
apps/accounts/           # пользователи
apps/games/              # модели Room, Game, Session
api/v1/accounts.py       # аутентификация
api/v1/games.py          # API игр
api/v1/urls.py           # маршруты
services/games/base.py   # абстрактный GameEngine
services/games/factory.py # фабрика
frontend/src/App.js      # обёртка
frontend/src/api/        # клиент
frontend/src/pages/Login.jsx
docs/TECH_DECISIONS.md   # история решений
docs/ROADMAP.md          # план (можешь переписать под свой)
```

---

### ⚠️ Лицензия GPLv3 — что важно знать

GAMESWARD распространяется под **GNU GPLv3** — лицензия с **«копилефт»**-эффектом.

**Что можно:**
- ✅ Брать код, менять, использовать.
- ✅ Публиковать свой проект на GitHub.
- ✅ Использовать для диплома, портфолио, коммерции.

**Что нужно:**
- ⚠️ **Сохранить GPLv3** в своём проекте (файл `LICENSE.md`).
- ⚠️ **Упомянуть** GAMESWARD в README.
- ⚠️ Если **распространяешь** (публикуешь, продаёшь) — **открыть исходники** своего проекта.

**Что нельзя:**
- ❌ Сделать **проприетарный** проект на базе GPLv3-кода (без переписывания).

**Пример упоминания в README:**
```markdown
## 🙏 Благодарности

Проект создан на базе [GAMESWARD](https://github.com/kvm64/GAMESWARD),
распространяется под лицензией [GPLv3](LICENSE.md).
```

**Если сомневаешься — спроси преподавателя.** Лучше уточнить заранее, чем переделывать.

---

### 🎯 Как выбрать?

**Ответь на 3 вопроса:**

1. **Хочу ли я, чтобы игра осталась в GAMESWARD надолго?**
   - Да → Путь A.
   - Нет → Путь B.

2. **Это дипломный проект или вклад в open-source?**
   - Диплом → Путь B.
   - Open-source → Путь A.

3. **Готов ли я соблюдать чужие правила (тесты, ревью, стиль)?**
   - Да → Путь A.
   - Нет → Путь B.

**Для большинства студентов — Путь B.** Он даёт **больше свободы** и **лучше подходит для диплома**.

**Путь A — для тех**, кто хочет **реальный вклад** в open-source и **не против** работать по правилам.

---

**Удачи!** 🚀 Твой форк — твоя песочница. Экспериментируй, ломай, чини, учись. И помни: **главное — не идеальный результат, а путь к нему.**