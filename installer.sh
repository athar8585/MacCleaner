#!/bin/bash

# Script d'installation automatique MacCleaner Pro 3.0
# Installation complète avec daemon autonome et interface moderne

set -e

# Couleurs pour l'affichage
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${PURPLE}🚀 MacCleaner Pro 3.0 - Installation Automatique${NC}"
echo "=================================================="
echo ""

# Vérifications système
echo -e "${BLUE}🔍 Vérifications système...${NC}"

# Vérifier macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo -e "${RED}❌ Ce script est conçu pour macOS uniquement${NC}"
    exit 1
fi

# Vérifier Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 requis. Installation:${NC}"
    echo "   brew install python3"
    exit 1
fi

echo -e "${GREEN}✅ Système compatible${NC}"

# Créer la structure d'installation
echo -e "${BLUE}📁 Création de la structure...${NC}"

INSTALL_DIR="$HOME/Applications/MacCleaner Pro"
CONFIG_DIR="$HOME/Library/Application Support/MacCleaner Pro"

mkdir -p "$INSTALL_DIR"
mkdir -p "$CONFIG_DIR"
mkdir -p "$CONFIG_DIR/quarantine"
mkdir -p "$CONFIG_DIR/backups"

# Copier les fichiers
echo -e "${BLUE}📄 Installation des fichiers...${NC}"

# Fichiers principaux
cp autonomous_cleaner.py "$INSTALL_DIR/"
cp modern_mac_cleaner.py "$INSTALL_DIR/"
cp daemon.py "$INSTALL_DIR/"
cp mac_cleaner.py "$INSTALL_DIR/"

# Scripts utilitaires
cp quick_clean.sh "$INSTALL_DIR/"
cp analyze_icloud.sh "$INSTALL_DIR/"

# Documentation
cp README.md "$INSTALL_DIR/"

# Créer l'environnement virtuel
echo -e "${BLUE}🐍 Configuration de l'environnement Python...${NC}"

cd "$INSTALL_DIR"
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install psutil schedule requests

echo -e "${GREEN}✅ Environnement Python configuré${NC}"

# Créer les scripts de lancement
echo -e "${BLUE}🔧 Création des lanceurs...${NC}"

# Script de lancement principal
cat > "$INSTALL_DIR/launch_cleaner.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python modern_mac_cleaner.py
EOF

chmod +x "$INSTALL_DIR/launch_cleaner.sh"

# Script de gestion du daemon
cat > "$INSTALL_DIR/manage_daemon.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python daemon.py "$@"
EOF

chmod +x "$INSTALL_DIR/manage_daemon.sh"

# Créer l'application macOS
echo -e "${BLUE}🍎 Création de l'application macOS...${NC}"

APP_DIR="$HOME/Applications/MacCleaner Pro.app"
mkdir -p "$APP_DIR/Contents/MacOS"
mkdir -p "$APP_DIR/Contents/Resources"

# Script exécutable de l'app
cat > "$APP_DIR/Contents/MacOS/MacCleaner Pro" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
./launch_cleaner.sh
EOF

chmod +x "$APP_DIR/Contents/MacOS/MacCleaner Pro"

# Info.plist pour l'app
cat > "$APP_DIR/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>MacCleaner Pro</string>
    <key>CFBundleIdentifier</key>
    <string>com.maccleanerpro.app</string>
    <key>CFBundleName</key>
    <string>MacCleaner Pro</string>
    <key>CFBundleDisplayName</key>
    <string>MacCleaner Pro 3.0</string>
    <key>CFBundleVersion</key>
    <string>3.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>3.0</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.utilities</string>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
</dict>
</plist>
EOF

# Configuration initiale
echo -e "${BLUE}⚙️ Configuration initiale...${NC}"

# Créer le fichier de configuration
cat > "$CONFIG_DIR/config.json" << 'EOF'
{
    "auto_clean_threshold": {
        "disk_usage_percent": 85,
        "available_space_gb": 10,
        "memory_usage_percent": 80
    },
    "schedule": {
        "daily_maintenance": "03:00",
        "weekly_deep_clean": "sunday:02:00",
        "malware_scan": "12:00"
    },
    "protection": {
        "icloud_protection": true,
        "important_files": true,
        "recent_files_days": 7
    },
    "malware_protection": {
        "enabled": true,
        "auto_quarantine": true,
        "scan_downloads": true,
        "real_time_protection": false
    },
    "ui_preferences": {
        "theme": "ios26",
        "notifications": true,
        "auto_start": false
    }
}
EOF

echo ""
echo -e "${GREEN}🎉 INSTALLATION TERMINÉE AVEC SUCCÈS !${NC}"
echo "============================================="
echo ""
echo -e "${PURPLE}📋 UTILISATION:${NC}"
echo ""
echo -e "${BLUE}🖥️ Interface Graphique:${NC}"
echo "   • Double-clic sur 'MacCleaner Pro.app' dans Applications"
echo ""
echo -e "${GREEN}🚀 Votre Mac est maintenant protégé par MacCleaner Pro 3.0 !${NC}"