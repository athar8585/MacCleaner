#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Installation MacCleaner Pro (mode rapide)"

REPO_URL="${MACCLEANER_REPO_URL:-https://github.com/your-user/MacCleaner.git}"
PREFIX="${HOME}/.maccleaner"
BIN_DIR="${HOME}/.local/bin"

echo "→ Dossier: $PREFIX"
if [ ! -d "$PREFIX" ]; then
  git clone --depth 1 "$REPO_URL" "$PREFIX"
else
  echo "→ Dépôt existant, mise à jour..."
  git -C "$PREFIX" pull --ff-only || true
fi

cd "$PREFIX"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
[ -f requirements.txt ] && pip install -r requirements.txt || pip install psutil

echo "→ Construction app (facultatif)"
[ -x build_app.sh ] && ./build_app.sh || true

mkdir -p "$BIN_DIR"
ln -sf "$PREFIX/run_cleaner.sh" "$BIN_DIR/maccleaner"

echo "✅ Install terminé. Ajoutez à votre PATH si nécessaire: $BIN_DIR"
echo "▶ Lancer: maccleaner" 