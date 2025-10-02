#!/bin/bash
set -e
APP="dist/MacCleaner Pro.app"
DMG="MacCleanerPro.dmg"
IDENTITY="Developer ID Application: CHANGE_ME (TEAMID)" # Remplacer par votre identité codesign

if [ ! -d "$APP" ]; then
  echo "Construire l'app d'abord (./build_app.sh)"; exit 1; fi

echo "🔏 Signature de l'app (ad hoc si identité non définie)"
if [[ "$IDENTITY" == *CHANGE_ME* ]]; then
  codesign --force --deep --sign - "$APP"
else
  codesign --force --deep --options runtime --sign "$IDENTITY" "$APP"
fi

codesign --verify --deep --strict "$APP" || { echo "❌ Vérification codesign échouée"; exit 1; }

echo "📦 Re-création DMG signé"
rm -f "$DMG"
./build_dmg.sh

if [[ "$IDENTITY" != *CHANGE_ME* ]]; then
  echo "🔏 Signature DMG"
  codesign --sign "$IDENTITY" "$DMG"
fi

echo "ℹ️ (Optionnel) Notarisation: xcrun notarytool submit $DMG --apple-id APPLE_ID --team-id TEAM_ID --password APP_SPECIFIC_PW --wait"

echo "✅ Signature terminée"
