#!/bin/bash
set -e
APP_NAME="MacCleaner Pro"
DIST_DIR="dist"
APP_DIR="$DIST_DIR/$APP_NAME.app"
echo "🛠  Construction de $APP_NAME (.app minimal)"
rm -rf "$DIST_DIR" && mkdir -p "$APP_DIR/Contents/MacOS" "$APP_DIR/Contents/Resources" logs
cat > "$APP_DIR/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>CFBundleExecutable</key><string>launcher</string>
<key>CFBundleIdentifier</key><string>com.maccleaner.pro</string>
<key>CFBundleName</key><string>MacCleaner Pro</string>
<key>CFBundleVersion</key><string>3.1.0</string>
<key>CFBundleShortVersionString</key><string>3.1.0</string>
<key>LSMinimumSystemVersion</key><string>10.14</string>
<key>LSApplicationCategoryType</key><string>public.app-category.utilities</string>
<key>NSHighResolutionCapable</key><true/>
</dict></plist>
PLIST
cat > "$APP_DIR/Contents/MacOS/launcher" <<'LAUNCH'
#!/bin/bash
cd "$(dirname "$0")/../../.."
if [ -d venv ]; then
  source venv/bin/activate
fi
exec python3 mac_cleaner.py "$@"
LAUNCH
chmod +x "$APP_DIR/Contents/MacOS/launcher"
echo "✅ Application créée: $APP_DIR"
