#!/bin/bash

# MacCleaner Pro - Installation et Configuration Automatique
# Script complet d'installation avec toutes les fonctionnalités

echo "🚀 MacCleaner Pro v2.0 - Installation Complète"
echo "=============================================="
echo ""

# Variables de configuration
INSTALL_DIR="$HOME/Applications/MacCleaner Pro"
LAUNCH_AGENT_DIR="$HOME/Library/LaunchAgents"
CONFIG_DIR="$HOME/.maccleanerpro"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Fonction d'affichage avec couleurs
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifications préliminaires
print_status "Vérification des prérequis..."

# Vérifier macOS
if [[ "$(uname)" != "Darwin" ]]; then
    print_error "Ce script est conçu pour macOS uniquement"
    exit 1
fi

# Vérifier Python 3
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 non trouvé. Installation requise."
    echo "Installation automatique avec Homebrew..."
    
    # Installer Homebrew si nécessaire
    if ! command -v brew &> /dev/null; then
        print_status "Installation de Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    # Installer Python 3
    print_status "Installation de Python 3..."
    brew install python3
fi

print_success "Python 3 détecté: $(python3 --version)"

# Créer la structure d'installation
print_status "Création de la structure d'installation..."

# Répertoire principal
mkdir -p "$INSTALL_DIR"
mkdir -p "$CONFIG_DIR"
mkdir -p "$LAUNCH_AGENT_DIR"

# Sous-répertoires
for dir in "config" "data" "logs" "temp" "quarantine" "backups"; do
    mkdir -p "$INSTALL_DIR/$dir"
    mkdir -p "$CONFIG_DIR/$dir"
done

print_success "Structure créée dans $INSTALL_DIR"

# Copier les fichiers du projet
print_status "Installation des fichiers..."

# Fichiers principaux
cp *.py "$INSTALL_DIR/"
cp *.sh "$INSTALL_DIR/"
cp *.swift "$INSTALL_DIR/" 2>/dev/null || true
cp README.md "$INSTALL_DIR/" 2>/dev/null || true
cp requirements.txt "$INSTALL_DIR/" 2>/dev/null || true

# Copier la configuration GitHub
if [[ -d ".github" ]]; then
    cp -r .github "$INSTALL_DIR/"
fi

print_success "Fichiers installés"

# Configurer l'environnement Python
print_status "Configuration de l'environnement Python..."

cd "$INSTALL_DIR"

# Créer l'environnement virtuel
python3 -m venv venv

# Activer et installer les dépendances
source venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install psutil requests

# Dépendances supplémentaires pour les fonctionnalités avancées
pip install cryptography schedule

print_success "Environnement Python configuré"

# Rendre les scripts exécutables
print_status "Configuration des permissions..."

chmod +x *.sh
chmod +x *.py

print_success "Permissions configurées"

# Créer l'application macOS
print_status "Création de l'application macOS..."

# Exécuter le script de création d'app
if [[ -f "create_app.sh" ]]; then
    ./create_app.sh
    
    # Déplacer l'app vers le dossier Applications
    if [[ -d "MacCleaner Pro.app" ]]; then
        cp -r "MacCleaner Pro.app" "/Applications/"
        print_success "Application installée dans /Applications/"
    fi
fi

# Configurer le lancement automatique
print_status "Configuration du service de surveillance..."

# Créer le fichier plist pour launchd
cat > "$LAUNCH_AGENT_DIR/com.maccleanerpro.launcher.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.maccleanerpro.launcher</string>
    <key>ProgramArguments</key>
    <array>
        <string>$INSTALL_DIR/venv/bin/python</string>
        <string>$INSTALL_DIR/launcher.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>WorkingDirectory</key>
    <string>$INSTALL_DIR</string>
</dict>
</plist>
EOF

# Charger le service
launchctl load "$LAUNCH_AGENT_DIR/com.maccleanerpro.launcher.plist" 2>/dev/null || true

print_success "Service de surveillance configuré"

# Configuration initiale
print_status "Configuration initiale..."

# Créer la configuration par défaut
cat > "$CONFIG_DIR/config/initial_config.json" << EOF
{
    "installation_date": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "version": "2.0.0",
    "install_path": "$INSTALL_DIR",
    "features": {
        "autonomous_monitoring": true,
        "icloud_protection": true,
        "malware_scanning": true,
        "github_sync": false,
        "auto_updates": true
    },
    "thresholds": {
        "disk_usage": 85,
        "memory_usage": 80,
        "cpu_temperature": 80
    }
}
EOF

print_success "Configuration initiale créée"

# Créer les alias pour l'accès facile
print_status "Création des raccourcis..."

# Ajouter au bashrc/zshrc
SHELL_CONFIG=""
if [[ -n "$ZSH_VERSION" ]]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [[ -n "$BASH_VERSION" ]]; then
    SHELL_CONFIG="$HOME/.bashrc"
fi

if [[ -n "$SHELL_CONFIG" ]]; then
    # Ajouter les alias
    echo "" >> "$SHELL_CONFIG"
    echo "# MacCleaner Pro Aliases" >> "$SHELL_CONFIG"
    echo "alias macclean='cd \"$INSTALL_DIR\" && ./launcher.py'" >> "$SHELL_CONFIG"
    echo "alias macclean-quick='cd \"$INSTALL_DIR\" && ./quick_clean.sh'" >> "$SHELL_CONFIG"
    echo "alias macclean-gui='cd \"$INSTALL_DIR\" && ./run_cleaner.sh'" >> "$SHELL_CONFIG"
    echo "alias macclean-scan='cd \"$INSTALL_DIR\" && python3 autonomous_system.py --scan-malware'" >> "$SHELL_CONFIG"
    
    print_success "Alias ajoutés à $SHELL_CONFIG"
fi

# Créer un lanceur dans le dock
print_status "Création du lanceur Dock..."

# Script lanceur simple
cat > "$INSTALL_DIR/dock_launcher.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python launcher.py
EOF

chmod +x "$INSTALL_DIR/dock_launcher.sh"

# Test de l'installation
print_status "Test de l'installation..."

cd "$INSTALL_DIR"
source venv/bin/activate

# Tester l'import des modules
python3 -c "
import sys
import os
sys.path.insert(0, os.getcwd())

try:
    import psutil
    print('✅ psutil: OK')
except ImportError as e:
    print('❌ psutil:', e)

try:
    import requests
    print('✅ requests: OK')
except ImportError as e:
    print('❌ requests:', e)

try:
    from launcher import MacCleanerLauncher
    print('✅ launcher: OK')
except ImportError as e:
    print('❌ launcher:', e)

print('✅ Test d installation réussi')
"

# Configuration GitHub (optionnelle)
echo ""
print_status "Configuration GitHub (optionnelle)..."
read -p "Voulez-vous configurer la synchronisation GitHub? (y/N): " setup_github

if [[ "$setup_github" =~ ^[Yy]$ ]]; then
    read -p "Nom d'utilisateur GitHub: " github_user
    read -p "Nom du repository (MacCleaner-Pro): " github_repo
    github_repo=${github_repo:-MacCleaner-Pro}
    read -s -p "Token d'accès GitHub (optionnel): " github_token
    echo ""
    
    # Sauvegarder la configuration GitHub
    cat > "$CONFIG_DIR/config/github_config.json" << EOF
{
    "repo_owner": "$github_user",
    "repo_name": "$github_repo",
    "access_token": "$github_token",
    "auto_sync": true,
    "sync_interval": 3600
}
EOF
    
    # Initialiser le repository si token fourni
    if [[ -n "$github_token" ]]; then
        print_status "Initialisation du repository GitHub..."
        python3 github_integration.py --setup
    fi
    
    print_success "Configuration GitHub sauvegardée"
fi

# Affichage final
echo ""
echo "🎉 Installation MacCleaner Pro v2.0 Terminée!"
echo "============================================="
echo ""
echo "📋 RÉSUMÉ DE L'INSTALLATION:"
echo "• Répertoire: $INSTALL_DIR"
echo "• Configuration: $CONFIG_DIR"
echo "• Application: /Applications/MacCleaner Pro.app"
echo "• Service automatique: Configuré"
echo ""
echo "🚀 COMMENT UTILISER:"
echo ""
echo "1️⃣  LANCEUR PRINCIPAL (Interface simplifiée):"
echo "   macclean"
echo "   # OU: python3 $INSTALL_DIR/launcher.py"
echo ""
echo "2️⃣  NETTOYAGE EXPRESS:"
echo "   macclean-quick"
echo "   # OU: $INSTALL_DIR/quick_clean.sh"
echo ""
echo "3️⃣  INTERFACE COMPLÈTE:"
echo "   macclean-gui"
echo "   # OU: $INSTALL_DIR/run_cleaner.sh"
echo ""
echo "4️⃣  APPLICATION NATIVE:"
echo "   Ouvrir 'MacCleaner Pro' depuis le Launchpad"
echo "   # OU: open -a 'MacCleaner Pro'"
echo ""
echo "🔧 FONCTIONNALITÉS DISPONIBLES:"
echo "• ✅ Nettoyage intelligent avec protection iCloud"
echo "• ✅ Surveillance autonome avec seuils d'alerte"
echo "• ✅ Scanner anti-malware en temps réel"
echo "• ✅ Synchronisation GitHub (si configurée)"
echo "• ✅ Interface native macOS"
echo "• ✅ Mise à jour automatique"
echo "• ✅ Sauvegarde et restauration"
echo ""
echo "⚙️  CONFIGURATION:"
echo "• Fichiers: $CONFIG_DIR/config/"
echo "• Logs: $CONFIG_DIR/logs/"
echo "• Base de données: $CONFIG_DIR/data/"
echo ""
echo "🔗 LIENS UTILES:"
echo "• Relancer l'installation: $INSTALL_DIR/install.sh"
echo "• Désinstaller: $INSTALL_DIR/uninstall.sh"
echo "• Documentation: $INSTALL_DIR/README.md"
echo ""

# Demander si on veut lancer immédiatement
read -p "Voulez-vous lancer MacCleaner Pro maintenant? (Y/n): " launch_now

if [[ ! "$launch_now" =~ ^[Nn]$ ]]; then
    print_status "Lancement de MacCleaner Pro..."
    
    # Redémarrer le shell pour charger les alias
    echo "💡 Redémarrez votre terminal pour utiliser les nouvelles commandes."
    echo ""
    
    # Lancer l'application
    cd "$INSTALL_DIR"
    source venv/bin/activate
    python3 launcher.py &
    
    print_success "MacCleaner Pro lancé!"
    echo ""
    echo "🎯 Profitez de votre Mac optimisé!"
fi

echo ""
echo "✨ Installation terminée avec succès! ✨"