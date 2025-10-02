#!/bin/bash
# Script de nettoyage d'urgence pour arrêter tous les processus Guardian

echo "🆘 MacCleaner - Nettoyage d'Urgence"
echo "=================================="

echo "🔍 Recherche des processus Guardian..."

# Afficher tous les processus liés à Guardian
echo "Processus trouvés :"
ps aux | grep -E "(guardian|instant_menubar|simple_guardian)" | grep -v grep

echo ""
echo "🛑 Arrêt de tous les processus Guardian..."

# Arrêter tous les processus guardian
pkill -f "guardian"
pkill -f "instant_menubar"
pkill -f "simple_guardian"

# Arrêter tous les osascript
killall osascript 2>/dev/null

# Supprimer les fichiers PID
rm -f /tmp/guardian*.pid
rm -f /tmp/simple_guardian.pid

echo "🧹 Nettoyage des fichiers temporaires..."

# Nettoyer les logs éventuels
rm -f /tmp/guardian*.log
rm -f /tmp/cleaner*.log

echo "✅ Nettoyage terminé !"
echo ""
echo "🔍 Vérification finale..."
ps aux | grep -E "(guardian|instant_menubar)" | grep -v grep

if [ $? -eq 1 ]; then
    echo "✅ Aucun processus Guardian détecté"
else
    echo "⚠️ Certains processus sont encore actifs"
fi

echo ""
echo "Vous pouvez maintenant relancer Guardian avec :"
echo "./launch_guardian.sh"