#!/bin/bash

# MacCleaner Pro - Script de Désinstallation
# Suppression complète et propre de MacCleaner Pro

echo "🗑️  MacCleaner Pro - Désinstallation"
echo "===================================="
echo ""

# Variables
INSTALL_DIR="$HOME/Applications/MacCleaner Pro"
CONFIG_DIR="$HOME/.maccleanerpro"
LAUNCH_AGENT_DIR="$HOME/Library/LaunchAgents"
APP_PATH="/Applications/MacCleaner Pro.app"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Confirmation
echo "⚠️  Cette action va supprimer complètement MacCleaner Pro de votre système."
echo ""
echo "📂 Éléments qui seront supprimés:"
echo "   • Application: $APP_PATH"
echo "   • Fichiers: $INSTALL_DIR"
echo "   • Configuration: $CONFIG_DIR"
echo "   • Services automatiques"
echo "   • Alias du shell"
echo ""
read -p "Êtes-vous sûr de vouloir continuer? (y/N): " confirm

if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "❌ Désinstallation annulée"
    exit 0
fi

echo ""
print_status "Début de la désinstallation..."

# Arrêter les services en cours
print_status "Arrêt des services..."

# Décharger le service launchd
if [[ -f "$LAUNCH_AGENT_DIR/com.maccleanerpro.launcher.plist" ]]; then
    launchctl unload "$LAUNCH_AGENT_DIR/com.maccleanerpro.launcher.plist" 2>/dev/null
    rm -f "$LAUNCH_AGENT_DIR/com.maccleanerpro.launcher.plist"
    print_success "Service launchd supprimé"
fi

# Terminer les processus MacCleaner Pro
pkill -f "maccleanerpro" 2>/dev/null
pkill -f "autonomous_system.py" 2>/dev/null
pkill -f "launcher.py" 2>/dev/null

print_success "Processus arrêtés"

# Supprimer l'application
print_status "Suppression de l'application..."

if [[ -d "$APP_PATH" ]]; then
    rm -rf "$APP_PATH"
    print_success "Application supprimée de /Applications/"
fi

# Supprimer les fichiers d'installation
print_status "Suppression des fichiers..."

if [[ -d "$INSTALL_DIR" ]]; then
    rm -rf "$INSTALL_DIR"
    print_success "Répertoire d'installation supprimé"
fi

# Sauvegarder la configuration avant suppression
print_status "Gestion de la configuration..."

backup_dir="$HOME/Desktop/MacCleaner_Backup_$(date +%Y%m%d_%H%M%S)"

if [[ -d "$CONFIG_DIR" ]]; then
    read -p "Voulez-vous sauvegarder votre configuration? (Y/n): " backup_config
    
    if [[ ! "$backup_config" =~ ^[Nn]$ ]]; then
        mkdir -p "$backup_dir"
        cp -r "$CONFIG_DIR" "$backup_dir/"
        print_success "Configuration sauvegardée dans $backup_dir"
    fi
    
    rm -rf "$CONFIG_DIR"
    print_success "Configuration supprimée"
fi

# Supprimer les alias du shell
print_status "Suppression des alias..."

for shell_config in "$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.bash_profile"; do
    if [[ -f "$shell_config" ]]; then
        # Supprimer les lignes MacCleaner Pro
        sed -i '' '/# MacCleaner Pro Aliases/,+4d' "$shell_config" 2>/dev/null
        print_success "Alias supprimés de $(basename "$shell_config")"
    fi
done

# Nettoyer le cache système
print_status "Nettoyage des caches..."

# Supprimer les caches de l'application
rm -rf "$HOME/Library/Caches/com.maccleanerpro"* 2>/dev/null
rm -rf "$HOME/Library/Application Support/MacCleaner Pro" 2>/dev/null
rm -rf "$HOME/Library/Preferences/com.maccleanerpro"* 2>/dev/null

print_success "Caches supprimés"

# Vérification finale
print_status "Vérification de la désinstallation..."

remaining_items=()

# Vérifier les éléments restants
[[ -d "$APP_PATH" ]] && remaining_items+=("Application macOS")
[[ -d "$INSTALL_DIR" ]] && remaining_items+=("Répertoire d'installation")
[[ -d "$CONFIG_DIR" ]] && remaining_items+=("Configuration")
[[ -f "$LAUNCH_AGENT_DIR/com.maccleanerpro.launcher.plist" ]] && remaining_items+=("Service launchd")

if [[ ${#remaining_items[@]} -eq 0 ]]; then
    print_success "Désinstallation complète réussie!"
else
    print_warning "Éléments restants détectés:"
    for item in "${remaining_items[@]}"; do
        echo "   • $item"
    done
fi

echo ""
echo "📊 RÉSUMÉ DE LA DÉSINSTALLATION:"
echo "================================"
echo ""
echo "✅ Éléments supprimés:"
echo "   • Application macOS"
echo "   • Fichiers d'installation"
echo "   • Services automatiques"
echo "   • Alias du shell"
echo "   • Caches système"
echo ""

if [[ -d "$backup_dir" ]]; then
    echo "💾 Sauvegarde créée:"
    echo "   • $backup_dir"
    echo ""
fi

echo "🔄 ACTIONS RECOMMANDÉES:"
echo "   • Redémarrez votre terminal pour supprimer les alias"
echo "   • Videz la corbeille pour libérer l'espace disque"
echo ""

if [[ ${#remaining_items[@]} -eq 0 ]]; then
    echo "🎉 MacCleaner Pro a été complètement désinstallé!"
else
    echo "⚠️  Quelques éléments n'ont pas pu être supprimés automatiquement."
    echo "   Vous pouvez les supprimer manuellement si nécessaire."
fi

echo ""
echo "🙏 Merci d'avoir utilisé MacCleaner Pro!"
echo ""

# Option de réinstallation
read -p "Voulez-vous télécharger la dernière version pour une réinstallation future? (y/N): " download_latest

if [[ "$download_latest" =~ ^[Yy]$ ]]; then
    print_status "Téléchargement de la dernière version..."
    
    download_dir="$HOME/Downloads/MacCleaner-Pro-Latest"
    mkdir -p "$download_dir"
    
    # Simuler le téléchargement (remplacer par la vraie URL GitHub)
    echo "💡 Téléchargez la dernière version depuis:"
    echo "   https://github.com/yourusername/MacCleaner-Pro/releases/latest"
    echo ""
    echo "📁 Ou clonez le repository:"
    echo "   git clone https://github.com/yourusername/MacCleaner-Pro.git"
    
    open "$download_dir"
fi

echo "👋 Au revoir et à bientôt!"