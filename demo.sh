#!/bin/bash

# Script de démonstration MacCleaner Pro
# Test du nettoyage en mode sécurisé (sans sudo)

echo "🧪 MacCleaner Pro - Mode Démonstration"
echo "======================================"
echo ""

# Créer des fichiers de test
echo "📁 Création de fichiers de test..."
mkdir -p ~/Desktop/MacCleaner_Test_Files
echo "Test cache file" > ~/Desktop/MacCleaner_Test_Files/cache.tmp
echo "Test log file" > ~/Desktop/MacCleaner_Test_Files/app.log
echo "Old download" > ~/Desktop/MacCleaner_Test_Files/old_download.zip

# Afficher l'état avant
echo "📊 État avant nettoyage:"
df -h / | head -2
echo ""

# Lancer le nettoyage rapide en mode sécurisé
echo "🚀 Lancement du nettoyage rapide..."
./quick_clean.sh

echo ""
echo "📊 État après nettoyage:"
df -h / | head -2

echo ""
echo "🧹 Nettoyage des fichiers de test..."
rm -rf ~/Desktop/MacCleaner_Test_Files

echo ""
echo "✅ Démonstration terminée !"
echo "💡 Pour utiliser MacCleaner Pro :"
echo "   • Interface graphique: ./run_cleaner.sh"
echo "   • Nettoyage rapide: ./quick_clean.sh"
echo "   • Application macOS: double-clic sur 'MacCleaner Pro.app'"