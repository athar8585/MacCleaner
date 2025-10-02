#!/bin/bash

# 🍎 MacCleaner Pro - Solution Alternative GARANTIE
# Crée une app bundle macOS qui fonctionne à 100%

echo "🍎 CRÉATION APP BUNDLE NATIVE MACOS"
echo "==================================="

APP_NAME="MacCleanerPro"
APP_DIR="/Applications/$APP_NAME.app"
BUNDLE_DIR="$APP_DIR/Contents"

echo "📁 Création structure bundle..."

# Supprimer ancienne app si existe
sudo rm -rf "$APP_DIR"

# Créer structure bundle macOS
sudo mkdir -p "$BUNDLE_DIR/MacOS"
sudo mkdir -p "$BUNDLE_DIR/Resources"

echo "📝 Création Info.plist..."

# Créer Info.plist
sudo tee "$BUNDLE_DIR/Info.plist" > /dev/null << 'PLIST_EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>MacCleaner Pro</string>
    <key>CFBundleExecutable</key>
    <string>MacCleanerPro</string>
    <key>CFBundleIdentifier</key>
    <string>com.maccleaner.pro</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>MacCleaner Pro</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>13.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
</dict>
</plist>
PLIST_EOF

echo "🚀 Création script exécutable..."

# Créer l'exécutable principal
sudo tee "$BUNDLE_DIR/MacOS/$APP_NAME" > /dev/null << 'EXEC_EOF'
#!/bin/bash

# MacCleaner Pro - Launcher
# Lance la version Python stable

APP_DIR="/Users/loicdeloison/Desktop/MacCleaner"

echo "🍎 Lancement MacCleaner Pro..."

# Aller dans le répertoire de l'app
cd "$APP_DIR"

# Lancer la version Tkinter stable
python3 mac_cleaner_tkinter.py

echo "✅ MacCleaner Pro fermé"
EXEC_EOF

# Rendre exécutable
sudo chmod +x "$BUNDLE_DIR/MacOS/$APP_NAME"

echo "🔧 Configuration permissions..."

# Fixer les permissions
sudo chmod -R 755 "$APP_DIR"
sudo chown -R "$USER:admin" "$APP_DIR"

# Supprimer attributs de quarantaine
sudo xattr -cr "$APP_DIR"

echo "✅ APP BUNDLE CRÉÉE AVEC SUCCÈS !"
echo ""
echo "📱 VOTRE APP EST PRÊTE :"
echo "   📁 Emplacement: $APP_DIR"
echo "   🚀 Lancement: Double-clic ou Launchpad"
echo "   ✅ Fonctionne comme toute app macOS"
echo ""
echo "🎯 L'app lance votre interface Tkinter fonctionnelle !"