#!/bin/bash
set -e
APP_NAME="MacCleaner Pro"
DMG_NAME="MacCleanerPro.dmg"
DIST_DIR="dist"
if [ ! -d "$DIST_DIR/$APP_NAME.app" ]; then
  echo "⚠️  Lancer d'abord ./build_app.sh"; exit 1; fi
rm -f "$DMG_NAME"
hdiutil create -volname "$APP_NAME" -srcfolder "$DIST_DIR" -ov -format UDZO "$DMG_NAME"
echo "✅ DMG créé: $DMG_NAME"
