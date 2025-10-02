#!/bin/bash

# Créateur d'application macOS pour MacCleaner Pro

APP_NAME="MacCleaner Pro"
APP_DIR="$APP_NAME.app"
CONTENTS_DIR="$APP_DIR/Contents"
MACOS_DIR="$CONTENTS_DIR/MacOS"
RESOURCES_DIR="$CONTENTS_DIR/Resources"

echo "🏗️  Création de l'application macOS..."

# Créer la structure de l'application
mkdir -p "$MACOS_DIR"
mkdir -p "$RESOURCES_DIR"

# Créer le script exécutable principal
cat > "$MACOS_DIR/$APP_NAME" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/../../../"
./run_cleaner.sh
EOF

chmod +x "$MACOS_DIR/$APP_NAME"

# Créer le fichier Info.plist
cat > "$CONTENTS_DIR/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>$APP_NAME</string>
    <key>CFBundleIdentifier</key>
    <string>com.maccleanerpro.app</string>
    <key>CFBundleName</key>
    <string>$APP_NAME</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.12</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.utilities</string>
</dict>
</plist>
EOF

# Créer une icône simple (optionnel)
cat > "$RESOURCES_DIR/icon.icns" << 'EOF'
# Icône placeholder - vous pouvez la remplacer par une vraie icône .icns
EOF

echo "✅ Application macOS créée : $APP_DIR"
echo "🖱️  Double-cliquez sur '$APP_DIR' pour lancer MacCleaner Pro"