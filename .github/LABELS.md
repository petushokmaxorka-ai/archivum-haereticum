# GitHub Labels для Архива Империума

> **3 верхнеуровневых списка** (по образцу GitHub Stars Lists) → **3 GitHub Labels** в репозитории.
> 
> Создаются один раз вручную (или через скрипт `scripts/create-github-labels.sh`).

## Три списка / Три labels

### ✨ Inspiration
- **Цвет**: `#FFD700` (золотой) или `#F1E05A` (жёлтый)
- **Описание**: Источник вдохновения для Архива (книга, фильм, лекция, миф, человек)
- **Соответствует**: `REPERTORIUM-INSPIRATION.md`

### 🚀 My stack
- **Цвет**: `#0E8A16` (зелёный)
- **Описание**: Завершённый артефакт Архива (досье / корпус / визуальная карта)
- **Соответствует**: `REPERTORIUM-MY-STACK.md`

### 🔮 Future ideas
- **Цвет**: `#5319E7` (фиолетовый)
- **Описание**: Идея для будущего досье / артефакта (ещё НЕ реализовано)
- **Соответствует**: `REPERTORIUM-FUTURE-IDEAS.md`

## Создание labels

### Вариант 1: через `gh` CLI (рекомендуется)

```bash
# После установки gh и авторизации
gh label create "inspiration" --color "FFD700" --description "Источник вдохновения для Архива"
gh label create "✨ inspiration" --color "F1E05A" --description "Источник вдохновения (с эмодзи)"
gh label create "my-stack" --color "0E8A16" --description "Завершённый артефакт"
gh label create "🚀 my-stack" --color "0E8A16" --description "Завершённый артефакт (с эмодзи)"
gh label create "future-ideas" --color "5319E7" --description "Идея для будущего"
gh label create "🔮 future-ideas" --color "5319E7" --description "Идея для будущего (с эмодзи)"
```

Или запустить скрипт:
```bash
bash scripts/create-github-labels.sh
```

### Вариант 2: вручную через GitHub UI

`https://github.com/petushokmaxorka-ai/archivum-haereticum/labels`

## Связь с Issue Templates

Когда labels созданы, работают Issue Templates:
- `.github/ISSUE_TEMPLATE/inspiration.md` → автоматически ставит `inspiration` + `✨ inspiration`
- `.github/ISSUE_TEMPLATE/my-stack.md` → автоматически ставит `my-stack` + `🚀 my-stack`
- `.github/ISSUE_TEMPLATE/future-ideas.md` → автоматически ставит `future-ideas` + `🔮 future-ideas`

## Метод

- **Новый источник** → Issue по шаблону `inspiration` → закрывается после добавления в `REPERTORIUM-INSPIRATION.md`
- **Новый артефакт** → Issue по шаблону `my-stack` → закрывается после добавления в `REPERTORIUM-MY-STACK.md`
- **Новая идея** → Issue по шаблону `future-ideas` → переходит в `my-stack` при реализации
