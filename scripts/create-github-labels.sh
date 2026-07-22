#!/usr/bin/env bash
# Создание 3 GitHub Labels для Архива Империума
# (соответствует 3 спискам в REPERTORIUM)
#
# Использование:
#   1. Установить gh CLI: https://cli.github.com/
#   2. Авторизоваться: gh auth login
#   3. Запустить: bash scripts/create-github-labels.sh

set -e

REPO="petushokmaxorka-ai/archivum-haereticum"

echo "🔮 Создаю 3 GitHub Labels для $REPO"
echo "   (соответствует 3 спискам в REPERTORIUM)"
echo

# Проверяем что gh установлен
if ! command -v gh &> /dev/null; then
  echo "❌ gh CLI не найден. Установите: https://cli.github.com/"
  exit 1
fi

# Проверяем авторизацию
if ! gh auth status &> /dev/null; then
  echo "❌ gh не авторизован. Запустите: gh auth login"
  exit 1
fi

# ✨ Inspiration (золотой)
echo "✨ Создаю label: inspiration"
gh label create "inspiration" \
  --repo "$REPO" \
  --color "FFD700" \
  --description "Источник вдохновения для Архива (книга, фильм, лекция, миф, человек)" \
  || gh label edit "inspiration" --repo "$REPO" --color "FFD700" --description "Источник вдохновения для Архива"

echo "✨ Создаю label: ✨ inspiration (с эмодзи)"
gh label create "✨ inspiration" \
  --repo "$REPO" \
  --color "F1E05A" \
  --description "Источник вдохновения (с эмодзи)" \
  || gh label edit "✨ inspiration" --repo "$REPO" --color "F1E05A" --description "Источник вдохновения (с эмодзи)"

# 🚀 My stack (зелёный)
echo "🚀 Создаю label: my-stack"
gh label create "my-stack" \
  --repo "$REPO" \
  --color "0E8A16" \
  --description "Завершённый артефакт Архива (досье / корпус / визуальная карта)" \
  || gh label edit "my-stack" --repo "$REPO" --color "0E8A16" --description "Завершённый артефакт Архива"

echo "🚀 Создаю label: 🚀 my-stack (с эмодзи)"
gh label create "🚀 my-stack" \
  --repo "$REPO" \
  --color "0E8A16" \
  --description "Завершённый артефакт (с эмодзи)" \
  || gh label edit "🚀 my-stack" --repo "$REPO" --color "0E8A16" --description "Завершённый артефакт (с эмодзи)"

# 🔮 Future ideas (фиолетовый)
echo "🔮 Создаю label: future-ideas"
gh label create "future-ideas" \
  --repo "$REPO" \
  --color "5319E7" \
  --description "Идея для будущего досье / артефакта (ещё НЕ реализовано)" \
  || gh label edit "future-ideas" --repo "$REPO" --color "5319E7" --description "Идея для будущего досье / артефакта"

echo "🔮 Создаю label: 🔮 future-ideas (с эмодзи)"
gh label create "🔮 future-ideas" \
  --repo "$REPO" \
  --color "5319E7" \
  --description "Идея для будущего (с эмодзи)" \
  || gh label edit "🔮 future-ideas" --repo "$REPO" --color "5319E7" --description "Идея для будущего (с эмодзи)"

echo
echo "✅ Все labels созданы!"
echo
echo "Созданные labels:"
gh label list --repo "$REPO" | grep -E "inspiration|my-stack|future-ideas" || echo "(проверьте: gh label list --repo $REPO)"

echo
echo "📋 Issue Templates готовы в .github/ISSUE_TEMPLATE/:"
echo "  - inspiration.md (✨)"
echo "  - my-stack.md (🚀)"
echo "  - future-ideas.md (🔮)"
echo
echo "🎯 Теперь при создании Issue в GitHub будут доступны 3 шаблона."
