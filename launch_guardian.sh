#!/bin/bash
# Script de lancement sécurisé pour Guardian

echo "🛡️ MacCleaner Guardian - Lancement Sécurisé"
echo "=========================================="

cd /Users/loicdeloison/Desktop/MacCleaner

# Vérifier si Guardian tourne déjà
if [ -f "/tmp/guardian_stable.pid" ]; then
    PID=$(cat /tmp/guardian_stable.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "⚠️  Guardian est déjà actif (PID: $PID)"
        echo "Voulez-vous l'arrêter d'abord ? (y/n)"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            python3 guardian_stable.py --stop
            sleep 2
        else
            echo "Lancement annulé"
            exit 1
        fi
    else
        echo "🧹 Nettoyage du fichier PID obsolète"
        rm -f /tmp/guardian_stable.pid
    fi
fi

# Nettoyer tous les processus guardian restants
echo "🧹 Nettoyage des processus guardian..."
pkill -f "guardian" > /dev/null 2>&1
pkill -f "instant_menubar" > /dev/null 2>&1
killall osascript > /dev/null 2>&1

echo "✅ Nettoyage terminé"
echo ""
echo "Choisissez le mode de lancement :"
echo "1. Mode daemon (arrière-plan)"
echo "2. Mode interactif (menu)"
echo "3. Juste vérifier le statut"

read -p "Votre choix (1-3): " choice

case $choice in
    1)
        echo "🚀 Lancement de Guardian en mode daemon..."
        python3 guardian_stable.py --daemon &
        sleep 2
        python3 guardian_stable.py --status
        ;;
    2)
        echo "🎛️ Lancement du menu interactif..."
        python3 guardian_stable.py --menu
        ;;
    3)
        echo "📊 Vérification du statut..."
        python3 guardian_stable.py --status
        ;;
    *)
        echo "❌ Choix invalide"
        exit 1
        ;;
esac