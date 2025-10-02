#!/bin/bash
# Script d'installation de MacCleaner Guardian dans la barre de menu

echo "🛡️  INSTALLATION MACCLEANER GUARDIAN MENUBAR"
echo "=============================================="

# Répertoire de travail
cd "$(dirname "$0")"

# Rendre les scripts exécutables
chmod +x guardian_menubar_simple.py

echo "✅ Scripts rendus exécutables"

# Créer le lanceur d'application barre de menu
cat > MacCleanerGuardianMenuBar.app/Contents/Info.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>MacCleaner Guardian</string>
    <key>CFBundleExecutable</key>
    <string>guardian_launch</string>
    <key>CFBundleIdentifier</key>
    <string>com.maccleaner.guardian.menubar</string>
    <key>CFBundleName</key>
    <string>MacCleanerGuardianMenuBar</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>LSUIElement</key>
    <true/>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
</dict>
</plist>
EOF

# Créer la structure de l'app bundle
mkdir -p MacCleanerGuardianMenuBar.app/Contents/MacOS
mkdir -p MacCleanerGuardianMenuBar.app/Contents/Resources

# Créer le script de lancement
cat > MacCleanerGuardianMenuBar.app/Contents/MacOS/guardian_launch << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/../../.."
exec python3 guardian_menubar_simple.py "$@"
EOF

chmod +x MacCleanerGuardianMenuBar.app/Contents/MacOS/guardian_launch

echo "✅ Application bundle créée"

# Créer le service LaunchAgent pour démarrage automatique
mkdir -p ~/Library/LaunchAgents

cat > ~/Library/LaunchAgents/com.maccleaner.guardian.menubar.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.maccleaner.guardian.menubar</string>
    <key>Program</key>
    <string>$(pwd)/MacCleanerGuardianMenuBar.app/Contents/MacOS/guardian_launch</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>ProcessType</key>
    <string>Interactive</string>
    <key>LimitLoadToSessionType</key>
    <string>Aqua</string>
    <key>WorkingDirectory</key>
    <string>$(pwd)</string>
    <key>StandardOutPath</key>
    <string>$(pwd)/guardian_menubar.log</string>
    <key>StandardErrorPath</key>
    <string>$(pwd)/guardian_menubar_error.log</string>
</dict>
</plist>
EOF

echo "✅ Service LaunchAgent créé"

# Proposer l'installation
echo ""
echo "🚀 OPTIONS D'INSTALLATION"
echo "=========================="
echo "1) Démarrage automatique avec macOS (Recommandé)"
echo "2) Lancement manuel seulement"
echo "3) Test direct"
echo ""
read -p "Choix (1/2/3): " choice

case $choice in
    1)
        echo "🔧 Installation du service de démarrage automatique..."
        
        # Charger le service
        launchctl unload ~/Library/LaunchAgents/com.maccleaner.guardian.menubar.plist 2>/dev/null
        launchctl load ~/Library/LaunchAgents/com.maccleaner.guardian.menubar.plist
        
        if [ $? -eq 0 ]; then
            echo "✅ Service installé avec succès!"
            echo ""
            echo "🎉 MacCleaner Guardian MenuBar est maintenant actif!"
            echo ""
            echo "📋 COMMENT L'UTILISER:"
            echo "• Surveillez les notifications macOS pour le statut"
            echo "• Cliquez sur les notifications pour accéder au menu"
            echo "• Le Guardian surveille automatiquement votre Mac"
            echo "• Icône 🛡️ = OK, 🟡 = Attention, ⚠️ = Action requise"
            echo ""
            echo "🔧 COMMANDES UTILES:"
            echo "• Menu rapide: python3 guardian_menubar_simple.py --menu"
            echo "• Statut: python3 guardian_menubar_simple.py --status"
            echo "• Nettoyage: python3 guardian_menubar_simple.py --cleanup"
            echo "• Arrêter service: launchctl unload ~/Library/LaunchAgents/com.maccleaner.guardian.menubar.plist"
            echo ""
            echo "Le Guardian démarrera automatiquement à chaque démarrage de macOS!"
        else
            echo "❌ Erreur installation service!"
        fi
        ;;
    2)
        echo "📋 INSTALLATION MANUELLE"
        echo ""
        echo "🎮 COMMANDES DISPONIBLES:"
        echo "• Lancer Guardian: python3 guardian_menubar_simple.py"
        echo "• Menu interactif: python3 guardian_menubar_simple.py --menu"
        echo "• Voir statut: python3 guardian_menubar_simple.py --status"
        echo "• Nettoyage rapide: python3 guardian_menubar_simple.py --cleanup"
        echo "• Optimisation: python3 guardian_menubar_simple.py --optimize"
        ;;
    3)
        echo "🧪 TEST DIRECT..."
        echo ""
        echo "Lancement de MacCleaner Guardian MenuBar..."
        python3 guardian_menubar_simple.py --menu
        ;;
    *)
        echo "❌ Choix invalide!"
        exit 1
        ;;
esac

echo ""
echo "🎉 INSTALLATION TERMINÉE!"
echo ""
echo "💡 FONCTIONNEMENT:"
echo "• Le Guardian fonctionne via les notifications macOS"
echo "• Pas d'icône fixe dans la barre de menu (plus discret)"
echo "• Notifications intelligentes selon l'état du système"
echo "• Menu interactif accessible via les notifications"
echo "• Surveillance continue en arrière-plan"
echo ""
echo "🔒 SÉCURITÉ:"
echo "• Nettoyage sécurisé uniquement"
echo "• Notifications avant actions automatiques"
echo "• Logs détaillés disponibles"
echo "• Configuration personnalisable"
echo ""
echo "Profitez de votre Mac optimisé automatiquement! 🚀"