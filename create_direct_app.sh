#!/bin/bash

# 🍎 MacCleaner Pro - Version Alternative Directe
# Crée une app qui lance directement sans Terminal

echo "🍎 CRÉATION APP ALTERNATIVE - LANCEMENT DIRECT"
echo "=============================================="

APP_NAME="MacCleanerPro_Direct"
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
    <string>MacCleaner Pro Direct</string>
    <key>CFBundleExecutable</key>
    <string>MacCleanerPro_Direct</string>
    <key>CFBundleIdentifier</key>
    <string>com.maccleaner.pro.direct</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>MacCleaner Pro Direct</string>
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
    <key>LSUIElement</key>
    <false/>
</dict>
</plist>
PLIST_EOF

echo "🚀 Création script exécutable direct..."

# Créer l'exécutable principal
sudo tee "$BUNDLE_DIR/MacOS/$APP_NAME" > /dev/null << 'EXEC_EOF'
#!/usr/bin/env python3

"""
MacCleaner Pro - Lanceur Direct
Lance l'interface directement sans passer par Terminal
"""

import os
import sys
import subprocess

def main():
    # Répertoire de l'application
    app_dir = "/Users/loicdeloison/Desktop/MacCleaner"
    
    # Changer vers le répertoire de l'app
    os.chdir(app_dir)
    
    # Lancer l'interface Tkinter
    try:
        subprocess.run([sys.executable, "mac_cleaner_tkinter.py"])
    except Exception as e:
        # Afficher erreur si problème
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Erreur MacCleaner Pro", 
            f"Impossible de lancer l'application:\n{str(e)}"
        )

if __name__ == "__main__":
    main()
EXEC_EOF

# Rendre exécutable
sudo chmod +x "$BUNDLE_DIR/MacOS/$APP_NAME"

echo "🔧 Configuration permissions..."

# Fixer les permissions
sudo chmod -R 755 "$APP_DIR"
sudo chown -R "$USER:admin" "$APP_DIR"

# Supprimer attributs de quarantaine
sudo xattr -cr "$APP_DIR"

echo "✅ APP DIRECTE CRÉÉE AVEC SUCCÈS !"
echo ""
echo "📱 NOUVELLE APP DISPONIBLE :"
echo "   📁 Nom: MacCleanerPro_Direct.app"
echo "   🚀 Lance directement l'interface Python"
echo "   ✅ Pas de Terminal intermédiaire"
echo ""
echo "🎯 Testez les deux apps pour voir laquelle fonctionne mieux !"