#!/bin/bash
set -e
VERSION="$1"
if [ -z "$VERSION" ]; then echo "Usage: $0 <version>"; exit 1; fi
if [ ! -f MacCleanerPro.dmg ]; then echo "DMG introuvable. Construire d'abord."; exit 1; fi

echo "🏷  Création tag v$VERSION"
git tag -a "v$VERSION" -m "Release $VERSION"
git push origin "v$VERSION"

echo "🚀 Publication (gh CLI nécessaire)"
if ! command -v gh >/dev/null 2>&1; then
  echo "Installer GitHub CLI (brew install gh) pour publier automatiquement"; exit 0; fi

gh release create "v$VERSION" MacCleanerPro.dmg \
  --title "MacCleaner Pro $VERSION" \
  --notes "Release $VERSION : améliorations performance, plugins, export rapports."

echo "✅ Release publiée"
