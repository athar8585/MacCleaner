#!/bin/bash

# 🎯 MacCleaner Pro - Lanceur Version Corrigée
# Ce script lance automatiquement la version qui fonctionne vraiment

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo "🚀 Lancement de MacCleaner Pro - Version Corrigée"
echo "================================================"
echo ""

# Vérifier si on a les versions corrigées
if [[ -f "mac_cleaner_ultra_simple.py" ]]; then
    echo "✅ Version ultra-simple disponible (garantie fonctionnelle)"
    echo "🎯 Lancement en cours..."
    echo ""
    python3 mac_cleaner_ultra_simple.py
elif [[ -f "mac_cleaner_fixed.py" ]]; then
    echo "✅ Version corrigée disponible"
    echo "🎯 Lancement en cours..."
    echo ""
    python3 mac_cleaner_fixed.py
else
    echo "⚠️ Versions corrigées non trouvées, utilisation de la version principale"
    echo "🎯 Lancement en cours..."
    echo ""
    python3 mac_cleaner.py
fi

echo ""
echo "👋 Merci d'avoir utilisé MacCleaner Pro !"