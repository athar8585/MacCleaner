#!/bin/bash
# Script d'installation automatique de MacCleaner Guardian

echo "🛡️  INSTALLATION MACCLEANER GUARDIAN"
echo "======================================"

# Vérification des permissions
if [ "$EUID" -eq 0 ]; then
    echo "❌ Ne pas exécuter en tant que root!"
    exit 1
fi

# Répertoire de travail
cd "$(dirname "$0")"

echo "📁 Répertoire actuel: $(pwd)"

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trouvé! Installation requise."
    exit 1
fi

echo "✅ Python 3 détecté: $(python3 --version)"

# Installer les dépendances Python
echo "📦 Installation des dépendances..."
pip3 install psutil schedule 2>/dev/null || echo "⚠️  Certaines dépendances peuvent être manquantes"

# Rendre exécutable
chmod +x maccleaner_guardian.py

# Test de lancement
echo "🧪 Test de lancement..."
if python3 maccleaner_guardian.py --help >/dev/null 2>&1; then
    echo "✅ Guardian fonctionnel!"
else
    echo "⚠️  Test échoué, mais installation continue..."
fi

# Proposer installation au démarrage
echo ""
echo "🚀 INSTALLATION COMME SERVICE DE DÉMARRAGE"
echo "=========================================="
echo "Voulez-vous installer MacCleaner Guardian comme service"
echo "qui se lance automatiquement au démarrage de macOS?"
echo ""
echo "1) Oui - Installation automatique au démarrage"
echo "2) Non - Installation manuelle seulement"
echo ""
read -p "Choix (1/2): " choice

case $choice in
    1)
        echo "🔧 Installation du service de démarrage..."
        python3 maccleaner_guardian.py --install
        
        if [ $? -eq 0 ]; then
            echo "✅ Service installé avec succès!"
            echo ""
            echo "📋 COMMANDES UTILES:"
            echo "• Panneau de contrôle: python3 maccleaner_guardian.py"
            echo "• Arrêter service: launchctl unload ~/Library/LaunchAgents/com.maccleaner.guardian.plist"
            echo "• Démarrer service: launchctl load ~/Library/LaunchAgents/com.maccleaner.guardian.plist"
            echo "• Désinstaller: python3 maccleaner_guardian.py --uninstall"
        else
            echo "❌ Erreur installation service!"
        fi
        ;;
    2)
        echo "📋 INSTALLATION MANUELLE TERMINÉE"
        echo ""
        echo "🎮 COMMANDES DISPONIBLES:"
        echo "• Panneau de contrôle: python3 maccleaner_guardian.py"
        echo "• Mode daemon: python3 maccleaner_guardian.py --daemon"
        echo "• Installer service: python3 maccleaner_guardian.py --install"
        ;;
    *)
        echo "❌ Choix invalide!"
        exit 1
        ;;
esac

echo ""
echo "🎉 INSTALLATION TERMINÉE!"
echo ""
echo "💡 UTILISATION:"
echo "• Ouvrez le panneau de contrôle: python3 maccleaner_guardian.py"
echo "• Le Guardian surveille votre Mac en arrière-plan"
echo "• Il vous notifie et nettoie automatiquement si nécessaire"
echo "• Configuration personnalisable dans l'interface"
echo ""
echo "🔒 SÉCURITÉ:"
echo "• Nettoyage sécurisé - pas de suppression système"
echo "• Notifications avant actions automatiques"
echo "• Logs détaillés dans ~/.maccleaner_guardian.log"
echo ""
echo "Profitez de votre Mac optimisé! 🚀"